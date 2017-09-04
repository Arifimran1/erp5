/*global window, rJS, RSVP */
/*jslint nomen: true, indent: 2, maxerr: 3 */
(function (window, rJS, RSVP) {
  "use strict";

  rJS(window)
    /////////////////////////////////////////////////////////////////
    // Acquired methods
    /////////////////////////////////////////////////////////////////
    .declareAcquiredMethod("updateHeader", "updateHeader")
    .declareAcquiredMethod("getUrlParameter", "getUrlParameter")
    .declareAcquiredMethod("getUrlFor", "getUrlFor")
    .declareAcquiredMethod("jio_put", "jio_put")
    .declareAcquiredMethod("notifySubmitting", "notifySubmitting")
    .declareAcquiredMethod("notifySubmitted", 'notifySubmitted')

    /////////////////////////////////////////////////////////////////
    // declared methods
    /////////////////////////////////////////////////////////////////

    .declareMethod("render", function (options) {
      return this.changeState({
        jio_key: options.jio_key,
        doc: options.doc,
        editable: options.editable ? 1 : 0
      });
    })

    .onEvent('submit', function () {
      var gadget = this;
      return gadget.notifySubmitting()
        .push(function () {
          return gadget.getDeclaredGadget('form_view');
        })
        .push(function (form_gadget) {
          return form_gadget.getContent();
        })
        .push(function (content) {
          var doc;
          if (!gadget.state.editable) {
            doc = content;
            content.portal_type = gadget.state.doc.portal_type;
            content.parent_relative_url = gadget.state.doc.parent_relative_url;
            content.text_content = gadget.state.doc.text_content;
          } else {
            doc = gadget.state.doc;
            doc.text_content = content.text_content;
          }
          doc.modification_date = (new Date()).toISOString();
          return gadget.jio_put(gadget.state.jio_key, doc);
        })
        .push(function () {
          return RSVP.all([
            gadget.notifySubmitted('Data Updated')
          ]);
        });
    })

    .declareMethod("triggerSubmit", function () {
      return this.element.querySelector('button[type="submit"]').click();
    })

    .onStateChange(function () {
      var gadget = this;
      return gadget.getDeclaredGadget('form_view')
        .push(function (form_gadget) {
          var editable = gadget.state.editable;
          return form_gadget.render({
            erp5_document: {
              "_embedded": {"_view": {
                "my_title": {
                  "description": "",
                  "title": "Title",
                  "default": gadget.state.doc.title,
                  "css_class": "",
                  "required": 1,
                  "editable": 1 - editable,
                  "key": "title",
                  "hidden": editable,
                  "type": "StringField"
                },
                "my_reference": {
                  "description": "",
                  "title": "Reference",
                  "default": gadget.state.doc.reference,
                  "css_class": "",
                  "required": 0,
                  "editable": 1 - editable,
                  "key": "reference",
                  "hidden": editable,
                  "type": "StringField"
                },
                "my_version": {
                  "description": "",
                  "title": "Version",
                  "default": gadget.state.doc.version,
                  "css_class": "",
                  "required": 0,
                  "editable": 1 - editable,
                  "key": "version",
                  "hidden": editable,
                  "type": "StringField"
                },
                "my_language": {
                  "description": "",
                  "title": "Language",
                  "default": gadget.state.doc.language,
                  "css_class": "",
                  "required": 0,
                  "editable": 1 - editable,
                  "key": "language",
                  "hidden": editable,
                  "type": "StringField"
                },
                "my_description": {
                  "description": "",
                  "title": "Description",
                  "default": gadget.state.doc.description,
                  "css_class": "",
                  "required": 0,
                  "editable": 1 - editable,
                  "key": "description",
                  "hidden": editable,
                  "type": "StringField"
                },
                "my_content": {
                  "default": gadget.state.doc.text_content,
                  "css_class": editable === 1 ? "content-iframe-maximize" : "",
                  "required": 0,
                  "editable": editable,
                  "key": "text_content",
                  "hidden": 0,
                  "type": editable === 1 ? "GadgetField" : "EditorField",
                  "url": "../officejs_ckeditor_gadget/app/",
                  "sandbox": "iframe"
                }
              }},
              "_links": {
                "type": {
                  // form_list display portal_type in header
                  name: ""
                }
              }
            },
            form_definition: {
              group_list: [[
                "left",
                [["my_title"], ["my_reference"], ["my_version"], ["my_language"], ["my_description"]]
              ], [
                "bottom",
                [["my_content"]]
              ]]
            }
          });
        })
        .push(function () {
          return RSVP.all([
            gadget.getUrlFor({command: 'history_previous'}),
            gadget.getUrlFor({command: 'selection_previous'}),
            gadget.getUrlFor({command: 'selection_next'}),
            gadget.getUrlFor({command: "change", options: {editable: true}})
          ]);
        })
        .push(function (url_list) {
          var header_dict = {
            page_title: gadget.state.doc.title,
            selection_url: url_list[0],
            save_action: true
          };
          if (!gadget.state.editable) {
            header_dict.previous_url = url_list[1];
            header_dict.next_url = url_list[2];
            header_dict.edit_content = url_list[3];
          }
          return gadget.updateHeader(header_dict);
        });
    });
}(window, rJS, RSVP));
