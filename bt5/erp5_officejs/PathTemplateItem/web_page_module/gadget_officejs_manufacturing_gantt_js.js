/*global window, rJS, RSVP, console */
/*jslint nomen: true, indent: 2 */
(function (window, rJS, RSVP) {
  "use strict";

  /////////////////////////////////////////////////////////////////
  // templates
  /////////////////////////////////////////////////////////////////
  var gadget_klass = rJS(window);


  /////////////////////////////////////////////////////////////////
  // some methods
  /////////////////////////////////////////////////////////////////

  gadget_klass

    /////////////////////////////////////////////////////////////////
    // ready
    /////////////////////////////////////////////////////////////////
    .ready(function (gadget) {
      gadget.property_dict = {};
    })

    /////////////////////////////////////////////////////////////////
    // published methods
    /////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////
    // acquired methods
    /////////////////////////////////////////////////////////////////
    .declareAcquiredMethod("jio_allDocs", "jio_allDocs")
    /////////////////////////////////////////////////////////////////
    // declared methods
    /////////////////////////////////////////////////////////////////
    .declareMethod('render', function (option_dict) {


      var gadget = this,
          container,
          graph_data_and_parameter,
          chart;
      gadget.property_dict.option_dict = option_dict.value;

      console.log("gantt option_dict", option_dict.value);
      gadget.renderGantt(); //Launched as service, not blocking
    })
    .declareJob("renderGantt", function () {
      var gadget = this,
          option_dict = gadget.property_dict.option_dict;
      return gadget.declareGadget(
        "unsafe/gadget_officejs_widget_gantt_dhtmlx.html",
        {scope: "gantt",
         sandbox: "iframe",
         element: gadget.element.querySelector(".gantt-content")
      })
      .push(function (gantt_widget) {
        // First search all production report not finished to find out the
        // list of production orders still having work on them
        var query;
        gadget.property_dict.gantt_widget = gantt_widget;
        console.log("gantt_widget", gantt_widget);
        query = 'portal_type:="Manufacturing Execution" AND NOT simulation_state: ("draft", "cancelled", "delivered")';
        return gadget.jio_allDocs({
          query: query,
          limit: 10000,
          sort_on: [['delivery.start_date', 'ascending']],
          select_list: ['reference', 'title', 'start_date', 'stop_date', 'uid', 'causality_uid']
        });
      })
      .push(function (delivery_list) {
        var causality_uid_list = [0], // Initiliaze with 0 to make sure to have at least one uid to search for
            i, delivery, query;

        delivery_list = delivery_list.data.rows;
        for (i = 0; i < delivery_list.length; i = i + 1) {
          delivery = delivery_list[i].value;
          if (causality_uid_list.indexOf(delivery.causality_uid) === -1) {
            causality_uid_list.push(delivery.causality_uid);
          }
        }
        query = 'portal_type:="Manufacturing Execution" AND causality_uid: (' + causality_uid_list.join(', ') + ') AND NOT simulation_state: ("draft", "cancelled")';
        console.log("QUERY", query);
        return gadget.jio_allDocs({
          query: query,
          limit: 10000,
          sort_on: [['delivery.start_date', 'ascending']],
          select_list: ['reference', 'title', 'start_date', 'stop_date', 'uid', 'causality_uid', 'causality_title']
        });
      })
      .push(function (delivery_list) {
        var i, delivery, causality_list = [],
            causality_dict = {}, causality_data,
            gantt_data = {},
            tree_list = [],
            data_list = [],
            sale_order_uid,
            delivery_data, tree_data;
        delivery_list = delivery_list.data.rows;
        for (i = 0; i < delivery_list.length; i = i + 1) {
          delivery = delivery_list[i].value;
          if (delivery.causality_uid !== undefined) {
            if (causality_list.indexOf(delivery.causality_uid) === -1) {
              causality_list.push(delivery.causality_uid);
            }
            causality_data = causality_dict[delivery.causality_uid] || {'start_date': new Date(delivery.start_date),
                                                                        'stop_date': new Date(delivery.stop_date),
                                                                        'title': delivery.causality_title,
                                                                        'type': 'project',
                                                                        'id': delivery.causality_uid};
            causality_data.start_date = new Date(Math.min.apply(
                null, [causality_data.start_date, new Date(delivery.start_date)]));
            causality_data.stop_date = new Date(Math.max.apply(
                null, [causality_data.stop_date, new Date(delivery.stop_date)]));
            causality_dict[delivery.causality_uid] = causality_data;
          }
          if (i === 0) {
            // We assume that by the sort on order_reference that the first line is a level 1 line
            sale_order_uid = delivery.parent_uid;
          }
          if (delivery.start_date !== undefined && delivery.stop_date !== undefined) {
            delivery_data = {'title': delivery.title,
                         'id': delivery.uid,
                         //'tree_id': delivery.uid,
                         'parent_id': delivery.causality_uid,
                         'start_date': delivery.start_date,
                         'stop_date': delivery.stop_date};
            if (delivery.parent_uid !== sale_order_uid) {
              delivery_data.parent_id = delivery.parent_uid;
            }
            data_list.push(delivery_data);
          }
        }
        for (i = 0; i < causality_list.length; i = i + 1) {
          causality_data = causality_dict[causality_list[i]];
          data_list.push(causality_data);
        }
        gantt_data.data_list = data_list;
        console.log("gantt_data", gantt_data);
        return gadget.property_dict.gantt_widget.render(gantt_data);
      });
    });


}(window, rJS, RSVP));