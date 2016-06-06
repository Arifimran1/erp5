<?xml version="1.0"?>
<ZopeData>
  <record id="1" aka="AAAAAAAAAAE=">
    <pickle>
      <global name="File" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>_Cacheable__manager_id</string> </key>
            <value> <string>http_cache</string> </value>
        </item>
        <item>
            <key> <string>_EtagSupport__etag</string> </key>
            <value> <string>ts83646620.56</string> </value>
        </item>
        <item>
            <key> <string>__name__</string> </key>
            <value> <string>worker-coffee.js</string> </value>
        </item>
        <item>
            <key> <string>content_type</string> </key>
            <value> <string>application/javascript</string> </value>
        </item>
        <item>
            <key> <string>data</string> </key>
            <value>
              <persistent> <string encoding="base64">AAAAAAAAAAI=</string> </persistent>
            </value>
        </item>
        <item>
            <key> <string>precondition</string> </key>
            <value> <string></string> </value>
        </item>
        <item>
            <key> <string>size</string> </key>
            <value> <int>339257</int> </value>
        </item>
        <item>
            <key> <string>title</string> </key>
            <value> <string></string> </value>
        </item>
      </dictionary>
    </pickle>
  </record>
  <record id="2" aka="AAAAAAAAAAI=">
    <pickle>
      <global name="Pdata" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

"no use strict";\n
;(function(window) {\n
if (typeof window.window != "undefined" && window.document) {\n
    return;\n
}\n
\n
window.console = function() {\n
    var msgs = Array.prototype.slice.call(arguments, 0);\n
    postMessage({type: "log", data: msgs});\n
};\n
window.console.error =\n
window.console.warn = \n
window.console.log =\n
window.console.trace = window.console;\n
\n
window.window = window;\n
window.ace = window;\n
\n
window.normalizeModule = function(parentId, moduleName) {\n
    if (moduleName.indexOf("!") !== -1) {\n
        var chunks = moduleName.split("!");\n
        return window.normalizeModule(parentId, chunks[0]) + "!" + window.normalizeModule(parentId, chunks[1]);\n
    }\n
    if (moduleName.charAt(0) == ".") {\n
        var base = parentId.split("/").slice(0, -1).join("/");\n
        moduleName = (base ? base + "/" : "") + moduleName;\n
        \n
        while(moduleName.indexOf(".") !== -1 && previous != moduleName) {\n
            var previous = moduleName;\n
            moduleName = moduleName.replace(/^\\.\\//, "").replace(/\\/\\.\\//, "/").replace(/[^\\/]+\\/\\.\\.\\//, "");\n
        }\n
    }\n
    \n
    return moduleName;\n
};\n
\n
window.require = function(parentId, id) {\n
    if (!id) {\n
        id = parentId\n
        parentId = null;\n
    }\n
    if (!id.charAt)\n
        throw new Error("worker.js require() accepts only (parentId, id) as arguments");\n
\n
    id = window.normalizeModule(parentId, id);\n
\n
    var module = window.require.modules[id];\n
    if (module) {\n
        if (!module.initialized) {\n
            module.initialized = true;\n
            module.exports = module.factory().exports;\n
        }\n
        return module.exports;\n
    }\n
    \n
    var chunks = id.split("/");\n
    if (!window.require.tlns)\n
        return console.log("unable to load " + id);\n
    chunks[0] = window.require.tlns[chunks[0]] || chunks[0];\n
    var path = chunks.join("/") + ".js";\n
    \n
    window.require.id = id;\n
    importScripts(path);\n
    return window.require(parentId, id);\n
};\n
window.require.modules = {};\n
window.require.tlns = {};\n
\n
window.define = function(id, deps, factory) {\n
    if (arguments.length == 2) {\n
        factory = deps;\n
        if (typeof id != "string") {\n
            deps = id;\n
            id = window.require.id;\n
        }\n
    } else if (arguments.length == 1) {\n
        factory = id;\n
        deps = []\n
        id = window.require.id;\n
    }\n
\n
    if (!deps.length)\n
        deps = [\'require\', \'exports\', \'module\']\n
\n
    if (id.indexOf("text!") === 0) \n
        return;\n
    \n
    var req = function(childId) {\n
        return window.require(id, childId);\n
    };\n
\n
    window.require.modules[id] = {\n
        exports: {},\n
        factory: function() {\n
            var module = this;\n
            var returnExports = factory.apply(this, deps.map(function(dep) {\n
              switch(dep) {\n
                  case \'require\': return req\n
                  case \'exports\': return module.exports\n
                  case \'module\':  return module\n
                  default:        return req(dep)\n
              }\n
            }));\n
            if (returnExports)\n
                module.exports = returnExports;\n
            return module;\n
        }\n
    };\n
};\n
window.define.amd = {}\n
\n
window.initBaseUrls  = function initBaseUrls(topLevelNamespaces) {\n
    require.tlns = topLevelNamespaces;\n
}\n
\n
window.initSender = function initSender() {\n
\n
    var EventEmitter = window.require("ace/lib/event_emitter").EventEmitter;\n
    var oop = window.require("ace/lib/oop");\n
    \n
    var Sender = function() {};\n
    \n
    (function() {\n
        \n
        oop.implement(this, EventEmitter);\n
                \n
        this.callback = function(data, callbackId) {\n
            postMessage({\n
                type: "call",\n
                id: callbackId,\n
                data: data\n
            });\n
        };\n
    \n
        this.emit = function(name, data) {\n
            postMessage({\n
                type: "event",\n
                name: name,\n
                data: data\n
            });\n
        };\n
        \n
    }).call(Sender.prototype);\n
    \n
    return new Sender();\n
}\n
\n
window.main = null;\n
window.sender = null;\n
\n
window.onmessage = function(e) {\n
    var msg = e.data;\n
    if (msg.command) {\n
        if (main[msg.command])\n
            main[msg.command].apply(main, msg.args);\n
        else\n
            throw new Error("Unknown command:" + msg.command);\n
    }\n
    else if (msg.init) {        \n
        initBaseUrls(msg.tlns);\n
        require("ace/lib/es5-shim");\n
        sender = initSender();\n
        var clazz = require(msg.module)[msg.classname];\n
        main = new clazz(sender);\n
    } \n
    else if (msg.event && sender) {\n
        sender._emit(msg.event, msg.data);\n
    }\n
};\n
})(this);// https://github.com/kriskowal/es5-shim\n
\n
define(\'ace/lib/es5-shim\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
function Empty() {}\n
\n
if (!Function.prototype.bind) {\n
    Function.prototype.bind = function bind(that) { // .length is 1\n
        var target = this;\n
        if (typeof target != "function") {\n
            throw new TypeError("Function.prototype.bind called on incompatible " + target);\n
        }\n
        var args = slice.call(arguments, 1); // for normal call\n
        var bound = function () {\n
\n
            if (this instanceof bound) {\n
\n
                var result = target.apply(\n
                    this,\n
                    args.concat(slice.call(arguments))\n
                );\n
                if (Object(result) === result) {\n
                    return result;\n
                }\n
                return this;\n
\n
            } else {\n
                return target.apply(\n
                    that,\n
                    args.concat(slice.call(arguments))\n
                );\n
\n
            }\n
\n
        };\n
        if(target.prototype) {\n
            Empty.prototype = target.prototype;\n
            bound.prototype = new Empty();\n
            Empty.prototype = null;\n
        }\n
        return bound;\n
    };\n
}\n
var call = Function.prototype.call;\n
var prototypeOfArray = Array.prototype;\n
var prototypeOfObject = Object.prototype;\n
var slice = prototypeOfArray.slice;\n
var _toString = call.bind(prototypeOfObject.toString);\n
var owns = call.bind(prototypeOfObject.hasOwnProperty);\n
var defineGetter;\n
var defineSetter;\n
var lookupGetter;\n
var lookupSetter;\n
var supportsAccessors;\n
if ((supportsAccessors = owns(prototypeOfObject, "__defineGetter__"))) {\n
    defineGetter = call.bind(prototypeOfObject.__defineGetter__);\n
    defineSetter = call.bind(prototypeOfObject.__defineSetter__);\n
    lookupGetter = call.bind(prototypeOfObject.__lookupGetter__);\n
    lookupSetter = call.bind(prototypeOfObject.__lookupSetter__);\n
}\n
if ([1,2].splice(0).length != 2) {\n
    if(function() { // test IE < 9 to splice bug - see issue #138\n
        function makeArray(l) {\n
            var a = new Array(l+2);\n
            a[0] = a[1] = 0;\n
            return a;\n
        }\n
        var array = [], lengthBefore;\n
        \n
        array.splice.apply(array, makeArray(20));\n
        array.splice.apply(array, makeArray(26));\n
\n
        lengthBefore = array.length; //46\n
        array.splice(5, 0, "XXX"); // add one element\n
\n
        lengthBefore + 1 == array.length\n
\n
        if (lengthBefore + 1 == array.length) {\n
            return true;// has right splice implementation without bugs\n
        }\n
    }()) {//IE 6/7\n
        var array_splice = Array.prototype.splice;\n
        Array.prototype.splice = function(start, deleteCount) {\n
            if (!arguments.length) {\n
                return [];\n
            } else {\n
                return array_splice.apply(this, [\n
                    start === void 0 ? 0 : start,\n
                    deleteCount === void 0 ? (this.length - start) : deleteCount\n
                ].concat(slice.call(arguments, 2)))\n
            }\n
        };\n
    } else {//IE8\n
        Array.prototype.splice = function(pos, removeCount){\n
            var length = this.length;\n
            if (pos > 0) {\n
                if (pos > length)\n
                    pos = length;\n
            } else if (pos == void 0) {\n
                pos = 0;\n
            } else if (pos < 0) {\n
                pos = Math.max(length + pos, 0);\n
            }\n
\n
            if (!(pos+removeCount < length))\n
                removeCount = length - pos;\n
\n
            var removed = this.slice(pos, pos+removeCount);\n
            var insert = slice.call(arguments, 2);\n
            var add = insert.length;            \n
            if (pos === length) {\n
                if (add) {\n
                    this.push.apply(this, insert);\n
                }\n
            } else {\n
                var remove = Math.min(removeCount, length - pos);\n
                var tailOldPos = pos + remove;\n
                var tailNewPos = tailOldPos + add - remove;\n
                var tailCount = length - tailOldPos;\n
                var lengthAfterRemove = length - remove;\n
\n
                if (tailNewPos < tailOldPos) { // case A\n
                    for (var i = 0; i < tailCount; ++i) {\n
                        this[tailNewPos+i] = this[tailOldPos+i];\n
                    }\n
                } else if (tailNewPos > tailOldPos) { // case B\n
                    for (i = tailCount; i--; ) {\n
                        this[tailNewPos+i] = this[tailOldPos+i];\n
                    }\n
                } // else, add == remove (nothing to do)\n
\n
                if (add && pos === lengthAfterRemove) {\n
                    this.length = lengthAfterRemove; // truncate array\n
                    this.push.apply(this, insert);\n
                } else {\n
                    this.length = lengthAfterRemove + add; // reserves space\n
                    for (i = 0; i < add; ++i) {\n
                        this[pos+i] = insert[i];\n
                    }\n
                }\n
            }\n
            return removed;\n
        };\n
    }\n
}\n
if (!Array.isArray) {\n
    Array.isArray = function isArray(obj) {\n
        return _toString(obj) == "[object Array]";\n
    };\n
}\n
var boxedString = Object("a"),\n
    splitString = boxedString[0] != "a" || !(0 in boxedString);\n
\n
if (!Array.prototype.forEach) {\n
    Array.prototype.forEach = function forEach(fun /*, thisp*/) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                object,\n
            thisp = arguments[1],\n
            i = -1,\n
            length = self.length >>> 0;\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(); // TODO message\n
        }\n
\n
        while (++i < length) {\n
            if (i in self) {\n
                fun.call(thisp, self[i], i, object);\n
            }\n
        }\n
    };\n
}\n
if (!Array.prototype.map) {\n
    Array.prototype.map = function map(fun /*, thisp*/) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                object,\n
            length = self.length >>> 0,\n
            result = Array(length),\n
            thisp = arguments[1];\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(fun + " is not a function");\n
        }\n
\n
        for (var i = 0; i < length; i++) {\n
            if (i in self)\n
                result[i] = fun.call(thisp, self[i], i, object);\n
        }\n
        return result;\n
    };\n
}\n
if (!Array.prototype.filter) {\n
    Array.prototype.filter = function filter(fun /*, thisp */) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                    object,\n
            length = self.length >>> 0,\n
            result = [],\n
            value,\n
            thisp = arguments[1];\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(fun + " is not a function");\n
        }\n
\n
        for (var i = 0; i < length; i++) {\n
            if (i in self) {\n
                value = self[i];\n
                if (fun.call(thisp, value, i, object)) {\n
                    result.push(value);\n
                }\n
            }\n
        }\n
        return result;\n
    };\n
}\n
if (!Array.prototype.every) {\n
    Array.prototype.every = function every(fun /*, thisp */) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                object,\n
            length = self.length >>> 0,\n
            thisp = arguments[1];\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(fun + " is not a function");\n
        }\n
\n
        for (var i = 0; i < length; i++) {\n
            if (i in self && !fun.call(thisp, self[i], i, object)) {\n
                return false;\n
            }\n
        }\n
        return true;\n
    };\n
}\n
if (!Array.prototype.some) {\n
    Array.prototype.some = function some(fun /*, thisp */) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                object,\n
            length = self.length >>> 0,\n
            thisp = arguments[1];\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(fun + " is not a function");\n
        }\n
\n
        for (var i = 0; i < length; i++) {\n
            if (i in self && fun.call(thisp, self[i], i, object)) {\n
                return true;\n
            }\n
        }\n
        return false;\n
    };\n
}\n
if (!Array.prototype.reduce) {\n
    Array.prototype.reduce = function reduce(fun /*, initial*/) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                object,\n
            length = self.length >>> 0;\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(fun + " is not a function");\n
        }\n
        if (!length && arguments.length == 1) {\n
            throw new TypeError("reduce of empty array with no initial value");\n
        }\n
\n
        var i = 0;\n
        var result;\n
        if (arguments.length >= 2) {\n
            result = arguments[1];\n
        } else {\n
            do {\n
                if (i in self) {\n
                    result = self[i++];\n
                    break;\n
                }\n
                if (++i >= length) {\n
                    throw new TypeError("reduce of empty array with no initial value");\n
                }\n
            } while (true);\n
        }\n
\n
        for (; i < length; i++) {\n
            if (i in self) {\n
                result = fun.call(void 0, result, self[i], i, object);\n
            }\n
        }\n
\n
        return result;\n
    };\n
}\n
if (!Array.prototype.reduceRight) {\n
    Array.prototype.reduceRight = function reduceRight(fun /*, initial*/) {\n
        var object = toObject(this),\n
            self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                object,\n
            length = self.length >>> 0;\n
        if (_toString(fun) != "[object Function]") {\n
            throw new TypeError(fun + " is not a function");\n
        }\n
        if (!length && arguments.length == 1) {\n
            throw new TypeError("reduceRight of empty array with no initial value");\n
        }\n
\n
        var result, i = length - 1;\n
        if (arguments.length >= 2) {\n
            result = arguments[1];\n
        } else {\n
            do {\n
                if (i in self) {\n
                    result = self[i--];\n
                    break;\n
                }\n
                if (--i < 0) {\n
                    throw new TypeError("reduceRight of empty array with no initial value");\n
                }\n
            } while (true);\n
        }\n
\n
        do {\n
            if (i in this) {\n
                result = fun.call(void 0, result, self[i], i, object);\n
            }\n
        } while (i--);\n
\n
        return result;\n
    };\n
}\n
if (!Array.prototype.indexOf || ([0, 1].indexOf(1, 2) != -1)) {\n
    Array.prototype.indexOf = function indexOf(sought /*, fromIndex */ ) {\n
        var self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                toObject(this),\n
            length = self.length >>> 0;\n
\n
        if (!length) {\n
            return -1;\n
        }\n
\n
        var i = 0;\n
        if (arguments.length > 1) {\n
            i = toInteger(arguments[1]);\n
        }\n
        i = i >= 0 ? i : Math.max(0, length + i);\n
        for (; i < length; i++) {\n
            if (i in self && self[i] === sought) {\n
                return i;\n
            }\n
        }\n
        return -1;\n
    };\n
}\n
if (!Array.prototype.lastIndexOf || ([0, 1].lastIndexOf(0, -3) != -1)) {\n
    Array.prototype.lastIndexOf = function lastIndexOf(sought /*, fromIndex */) {\n
        var self = splitString && _toString(this) == "[object String]" ?\n
                this.split("") :\n
                toObject(this),\n
            length = self.length >>> 0;\n
\n
        if (!length) {\n
            return -1;\n
        }\n
        var i = length - 1;\n
        if (arguments.length > 1) {\n
            i = Math.min(i, toInteger(arguments[1]));\n
        }\n
        i = i >= 0 ? i : length - Math.abs(i);\n
        for (; i >= 0; i--) {\n
            if (i in self && sought === self[i]) {\n
                return i;\n
            }\n
        }\n
        return -1;\n
    };\n
}\n
if (!Object.getPrototypeOf) {\n
    Object.getPrototypeOf = function getPrototypeOf(object) {\n
        return object.__proto__ || (\n
            object.constructor ?\n
            object.constructor.prototype :\n
            prototypeOfObject\n
        );\n
    };\n
}\n
if (!Object.getOwnPropertyDescriptor) {\n
    var ERR_NON_OBJECT = "Object.getOwnPropertyDescriptor called on a " +\n
                         "non-object: ";\n
    Object.getOwnPropertyDescriptor = function getOwnPropertyDescriptor(object, property) {\n
        if ((typeof object != "object" && typeof object != "function") || object === null)\n
            throw new TypeError(ERR_NON_OBJECT + object);\n
        if (!owns(object, property))\n
            return;\n
\n
        var descriptor, getter, setter;\n
        descriptor =  { enumerable: true, configurable: true };\n
        if (supportsAccessors) {\n
            var prototype = object.__proto__;\n
            object.__proto__ = prototypeOfObject;\n
\n
            var getter = lookupGetter(object, property);\n
            var setter = lookupSetter(object, property);\n
            object.__proto__ = prototype;\n
\n
            if (getter || setter) {\n
                if (getter) descriptor.get = getter;\n
                if (setter) descriptor.set = setter;\n
                return descriptor;\n
            }\n
        }\n
        descriptor.value = object[property];\n
        return descriptor;\n
    };\n
}\n
if (!Object.getOwnPropertyNames) {\n
    Object.getOwnPropertyNames = function getOwnPropertyNames(object) {\n
        return Object.keys(object);\n
    };\n
}\n
if (!Object.create) {\n
    var createEmpty;\n
    if (Object.prototype.__proto__ === null) {\n
        createEmpty = function () {\n
            return { "__proto__": null };\n
        };\n
    } else {\n
        createEmpty = function () {\n
            var empty = {};\n
            for (var i in empty)\n
                empty[i] = null;\n
            empty.constructor =\n
            empty.hasOwnProperty =\n
            empty.propertyIsEnumerable =\n
            empty.isPrototypeOf =\n
            empty.toLocaleString =\n
            empty.toString =\n
            empty.valueOf =\n
            empty.__proto__ = null;\n
            return empty;\n
        }\n
    }\n
\n
    Object.create = function create(prototype, properties) {\n
        var object;\n
        if (prototype === null) {\n
            object = createEmpty();\n
        } else {\n
            if (typeof prototype != "object")\n
                throw new TypeError("typeof prototype["+(typeof prototype)+"] != \'object\'");\n
            var Type = function () {};\n
            Type.prototype = prototype;\n
            object = new Type();\n
            object.__proto__ = prototype;\n
        }\n
        if (properties !== void 0)\n
            Object.defineProperties(object, properties);\n
        return object;\n
    };\n
}\n
\n
function doesDefinePropertyWork(object) {\n
    try {\n
        Object.defineProperty(object, "sentinel", {});\n
        return "sentinel" in object;\n
    } catch (exception) {\n
    }\n
}\n
if (Object.defineProperty) {\n
    var definePropertyWorksOnObject = doesDefinePropertyWork({});\n
    var definePropertyWorksOnDom = typeof document == "undefined" ||\n
        doesDefinePropertyWork(document.createElement("div"));\n
    if (!definePropertyWorksOnObject || !definePropertyWorksOnDom) {\n
        var definePropertyFallback = Object.defineProperty;\n
    }\n
}\n
\n
if (!Object.defineProperty || definePropertyFallback) {\n
    var ERR_NON_OBJECT_DESCRIPTOR = "Property description must be an object: ";\n
    var ERR_NON_OBJECT_TARGET = "Object.defineProperty called on non-object: "\n
    var ERR_ACCESSORS_NOT_SUPPORTED = "getters & setters can not be defined " +\n
                                      "on this javascript engine";\n
\n
    Object.defineProperty = function defineProperty(object, property, descriptor) {\n
        if ((typeof object != "object" && typeof object != "function") || object === null)\n
            throw new TypeError(ERR_NON_OBJECT_TARGET + object);\n
        if ((typeof descriptor != "object" && typeof descriptor != "function") || descriptor === null)\n
            throw new TypeError(ERR_NON_OBJECT_DESCRIPTOR + descriptor);\n
        if (definePropertyFallback) {\n
            try {\n
                return definePropertyFallback.call(Object, object, property, descriptor);\n
            } catch (exception) {\n
            }\n
        }\n
        if (owns(descriptor, "value")) {\n
\n
            if (supportsAccessors && (lookupGetter(object, property) ||\n
                                      lookupSetter(object, property)))\n
            {\n
                var prototype = object.__proto__;\n
                object.__proto__ = prototypeOfObject;\n
                delete object[property];\n
                object[property] = descriptor.value;\n
                object.__proto__ = prototype;\n
            } else {\n
                object[property] = descriptor.value;\n
            }\n
        } else {\n
            if (!supportsAccessors)\n
                throw new TypeError(ERR_ACCESSORS_NOT_SUPPORTED);\n
            if (owns(descriptor, "get"))\n
                defineGetter(object, property, descriptor.get);\n
            if (owns(descriptor, "set"))\n
                defineSetter(object, property, descriptor.set);\n
        }\n
\n
        return object;\n
    };\n
}\n
if (!Object.defineProperties) {\n
    Object.defineProperties = function defineProperties(object, properties) {\n
        for (var property in properties) {\n
            if (owns(properties, property))\n
                Object.defineProperty(object, property, properties[property]);\n
        }\n
        return object;\n
    };\n
}\n
if (!Object.seal) {\n
    Object.seal = function seal(object) {\n
        return object;\n
    };\n
}\n
if (!Object.freeze) {\n
    Object.freeze = function freeze(object) {\n
        return object;\n
    };\n
}\n
try {\n
    Object.freeze(function () {});\n
} catch (exception) {\n
    Object.freeze = (function freeze(freezeObject) {\n
        return function freeze(object) {\n
            if (typeof object == "function") {\n
                return object;\n
            } else {\n
                return freezeObject(object);\n
            }\n
        };\n
    })(Object.freeze);\n
}\n
if (!Object.preventExtensions) {\n
    Object.preventExtensions = function preventExtensions(object) {\n
        return object;\n
    };\n
}\n
if (!Object.isSealed) {\n
    Object.isSealed = function isSealed(object) {\n
        return false;\n
    };\n
}\n
if (!Object.isFrozen) {\n
    Object.isFrozen = function isFrozen(object) {\n
        return false;\n
    };\n
}\n
if (!Object.isExtensible) {\n
    Object.isExtensible = function isExtensible(object) {\n
        if (Object(object) === object) {\n
            throw new TypeError(); // TODO message\n
        }\n
        var name = \'\';\n
        while (owns(object, name)) {\n
            name += \'?\';\n
        }\n
        object[name] = true;\n
        var returnValue = owns(object, name);\n
        delete object[name];\n
        return returnValue;\n
    };\n
}\n
if (!Object.keys) {\n
    var hasDontEnumBug = true,\n
        dontEnums = [\n
            "toString",\n
            "toLocaleString",\n
            "valueOf",\n
            "hasOwnProperty",\n
            "isPrototypeOf",\n
            "propertyIsEnumerable",\n
            "constructor"\n
        ],\n
        dontEnumsLength = dontEnums.length;\n
\n
    for (var key in {"toString": null}) {\n
        hasDontEnumBug = false;\n
    }\n
\n
    Object.keys = function keys(object) {\n
\n
        if (\n
            (typeof object != "object" && typeof object != "function") ||\n
            object === null\n
        ) {\n
            throw new TypeError("Object.keys called on a non-object");\n
        }\n
\n
        var keys = [];\n
        for (var name in object) {\n
            if (owns(object, name)) {\n
                keys.push(name);\n
            }\n
        }\n
\n
        if (hasDontEnumBug) {\n
            for (var i = 0, ii = dontEnumsLength; i < ii; i++) {\n
                var dontEnum = dontEnums[i];\n
                if (owns(object, dontEnum)) {\n
                    keys.push(dontEnum);\n
                }\n
            }\n
        }\n
        return keys;\n
    };\n
\n
}\n
if (!Date.now) {\n
    Date.now = function now() {\n
        return new Date().getTime();\n
    };\n
}\n
var ws = "\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\xA0\\u1680\\u180E\\u2000\\u2001\\u2002\\u2003" +\n
    "\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u202F\\u205F\\u3000\\u2028" +\n
    "\\u2029\\uFEFF";\n
if (!String.prototype.trim || ws.trim()) {\n
    ws = "[" + ws + "]";\n
    var trimBeginRegexp = new RegExp("^" + ws + ws + "*"),\n
        trimEndRegexp = new RegExp(ws + ws + "*$");\n
    String.prototype.trim = function trim() {\n
        return String(this).replace(trimBeginRegexp, "").replace(trimEndRegexp, "");\n
    };\n
}\n
\n
function toInteger(n) {\n
    n = +n;\n
    if (n !== n) { // isNaN\n
        n = 0;\n
    } else if (n !== 0 && n !== (1/0) && n !== -(1/0)) {\n
        n = (n > 0 || -1) * Math.floor(Math.abs(n));\n
    }\n
    return n;\n
}\n
\n
function isPrimitive(input) {\n
    var type = typeof input;\n
    return (\n
        input === null ||\n
        type === "undefined" ||\n
        type === "boolean" ||\n
        type === "number" ||\n
        type === "string"\n
    );\n
}\n
\n
function toPrimitive(input) {\n
    var val, valueOf, toString;\n
    if (isPrimitive(input)) {\n
        return input;\n
    }\n
    valueOf = input.valueOf;\n
    if (typeof valueOf === "function") {\n
        val = valueOf.call(input);\n
        if (isPrimitive(val)) {\n
            return val;\n
        }\n
    }\n
    toString = input.toString;\n
    if (typeof toString === "function") {\n
        val = toString.call(input);\n
        if (isPrimitive(val)) {\n
            return val;\n
        }\n
    }\n
    throw new TypeError();\n
}\n
var toObject = function (o) {\n
    if (o == null) { // this matches both null and undefined\n
        throw new TypeError("can\'t convert "+o+" to object");\n
    }\n
    return Object(o);\n
};\n
\n
});\n
\n
define(\'ace/mode/coffee_worker\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/worker/mirror\', \'ace/mode/coffee/coffee-script\'], function(require, exports, module) {\n
\n
\n
var oop = require("../lib/oop");\n
var Mirror = require("../worker/mirror").Mirror;\n
var coffee = require("../mode/coffee/coffee-script");\n
\n
window.addEventListener = function() {};\n
\n
\n
var Worker = exports.Worker = function(sender) {\n
    Mirror.call(this, sender);\n
    this.setTimeout(250);\n
};\n
\n
oop.inherits(Worker, Mirror);\n
\n
(function() {\n
\n
    this.onUpdate = function() {\n
        var value = this.doc.getValue();\n
\n
        try {\n
            coffee.parse(value).compile();\n
        } catch(e) {\n
            var loc = e.location;\n
            if (loc) {\n
                this.sender.emit("error", {\n
                    row: loc.first_line,\n
                    column: loc.first_column,\n
                    endRow: loc.last_line,\n
                    endColumn: loc.last_column,\n
                    text: e.message,\n
                    type: "error"\n
                });\n
            }\n
            return;\n
        }\n
        this.sender.emit("ok");\n
    };\n
\n
}).call(Worker.prototype);\n
\n
});\n
\n
define(\'ace/lib/oop\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
\n
exports.inherits = (function() {\n
    var tempCtor = function() {};\n
    return function(ctor, superCtor) {\n
        tempCtor.prototype = superCtor.prototype;\n
        ctor.super_ = superCtor.prototype;\n
        ctor.prototype = new tempCtor();\n
        ctor.prototype.constructor = ctor;\n
    };\n
}());\n
\n
exports.mixin = function(obj, mixin) {\n
    for (var key in mixin) {\n
        obj[key] = mixin[key];\n
    }\n
    return obj;\n
};\n
\n
exports.implement = function(proto, mixin) {\n
    exports.mixin(proto, mixin);\n
};\n
\n
});\n
define(\'ace/worker/mirror\', [\'require\', \'exports\', \'module\' , \'ace/document\', \'ace/lib/lang\'], function(require, exports, module) {\n
\n
\n
var Document = require("../document").Document;\n
var lang = require("../lib/lang");\n
    \n
var Mirror = exports.Mirror = function(sender) {\n
    this.sender = sender;\n
    var doc = this.doc = new Document("");\n
    \n
    var deferredUpdate = this.deferredUpdate = lang.delayedCall(this.onUpdate.bind(this));\n
    \n
    var _self = this;\n
    sender.on("change", function(e) {\n
        doc.applyDeltas(e.data);\n
        deferredUpdate.schedule(_self.$timeout);\n
    });\n
};\n
\n
(function() {\n
    \n
    this.$timeout = 500;\n
    \n
    this.setTimeout = function(timeout) {\n
        this.$timeout = timeout;\n
    };\n
    \n
    this.setValue = function(value) {\n
        this.doc.setValue(value);\n
        this.deferredUpdate.schedule(this.$timeout);\n
    };\n
    \n
    this.getValue = function(callbackId) {\n
        this.sender.callback(this.doc.getValue(), callbackId);\n
    };\n
    \n
    this.onUpdate = function() {\n
    };\n
    \n
}).call(Mirror.prototype);\n
\n
});\n
\n
define(\'ace/document\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/lib/event_emitter\', \'ace/range\', \'ace/anchor\'], function(require, exports, module) {\n
\n
\n
var oop = require("./lib/oop");\n
var EventEmitter = require("./lib/event_emitter").EventEmitter;\n
var Range = require("./range").Range;\n
var Anchor = require("./anchor").Anchor;\n
\n
var Document = function(text) {\n
    this.$lines = [];\n
    if (text.length == 0) {\n
        this.$lines = [""];\n
    } else if (Array.isArray(text)) {\n
        this._insertLines(0, text);\n
    } else {\n
        this.insert({row: 0, column:0}, text);\n
    }\n
};\n
\n
(function() {\n
\n
    oop.implement(this, EventEmitter);\n
    this.setValue = function(text) {\n
        var len = this.getLength();\n
        this.remove(new Range(0, 0, len, this.getLine(len-1).length));\n
        this.insert({row: 0, column:0}, text);\n
    };\n
    this.getValue = function() {\n
        return this.getAllLines().join(this.getNewLineCharacter());\n
    };\n
    this.createAnchor = function(row, column) {\n
        return new Anchor(this, row, column);\n
    };\n
    if ("aaa".split(/a/).length == 0)\n
        this.$split = function(text) {\n
            return text.replace(/\\r\\n|\\r/g, "\\n").split("\\n");\n
        }\n
    else\n
        this.$split = function(text) {\n
            return text.split(/\\r\\n|\\r|\\n/);\n
        };\n
\n
\n
    this.$detectNewLine = function(text) {\n
        var match = text.match(/^.*?(\\r\\n|\\r|\\n)/m);\n
        this.$autoNewLine = match ? match[1] : "\\n";\n
    };\n
    this.getNewLineCharacter = function() {\n
        switch (this.$newLineMode) {\n
          case "windows":\n
            return "\\r\\n";\n
          case "unix":\n
            return "\\n";\n
          default:\n
            return this.$autoNewLine;\n
        }\n
    };\n
\n
    this.$autoNewLine = "\\n";\n
    this.$newLineMode = "auto";\n
    this.setNewLineMode = function(newLineMode) {\n
        if (this.$newLineMode === newLineMode)\n
            return;\n
\n
        this.$newLineMode = newLineMode;\n
    };\n
    this.getNewLineMode = function() {\n
        return this.$newLineMode;\n
    };\n
    this.isNewLine = function(text) {\n
        return (text == "\\r\\n" || text == "\\r" || text == "\\n");\n
    };\n
    this.getLine = function(row) {\n
        return this.$lines[row] || "";\n
    };\n
    this.getLines = function(firstRow, lastRow) {\n
        return this.$lines.slice(firstRow, lastRow + 1);\n
    };\n
    this.getAllLines = function() {\n
        return this.getLines(0, this.getLength());\n
    };\n
    this.getLength = function() {\n
        return this.$lines.length;\n
    };\n
    this.getTextRange = function(range) {\n
        if (range.start.row == range.end.row) {\n
            return this.getLine(range.start.row)\n
                .substring(range.start.column, range.end.column);\n
        }\n
        var lines = this.getLines(range.start.row, range.end.row);\n
        lines[0] = (lines[0] || "").substring(range.start.column);\n
        var l = lines.length - 1;\n
        if (range.end.row - range.start.row == l)\n
            lines[l] = lines[l].substring(0, range.end.column);\n
        return lines.join(this.getNewLineCharacter());\n
    };\n
\n
    this.$clipPosition = function(position) {\n
        var length = this.getLength();\n
        if (position.row >= length) {\n
            position.row = Math.max(0, length - 1);\n
            position.column = this.getLine(length-1).length;\n
        } else if (position.row < 0)\n
            position.row = 0;\n
        return position;\n
    };\n
    this.insert = function(position, text) {\n
        if (!text || text.length === 0)\n
            return position;\n
\n
        position = this.$clipPosition(position);\n
        if (this.getLength() <= 1)\n
            this.$detectNewLine(text);\n
\n
        var lines = this.$split(text);\n
        var firstLine = lines.splice(0, 1)[0];\n
        var lastLine = lines.length == 0 ? null : lines.splice(lines.length - 1, 1)[0];\n
\n
        position = this.insertInLine(position, firstLine);\n
        if (lastLine !== null) {\n
            position = this.insertNewLine(position); // terminate first line\n
            position = this._insertLines(position.row, lines);\n
            position = this.insertInLine(position, lastLine || "");\n
        }\n
        return position;\n
    };\n
    this.insertLines = function(row, lines) {\n
        if (row >= this.getLength())\n
            return this.insert({row: row, column: 0}, "\\n" + lines.join("\\n"));\n
        return this._insertLines(Math.max(row, 0), lines);\n
    };\n
    this._insertLines = function(row, lines) {\n
        if (lines.length == 0)\n
            return {row: row, column: 0};\n
        if (lines.length > 0xFFFF) {\n
            var end = this._insertLines(row, lines.slice(0xFFFF));\n
            lines = lines.slice(0, 0xFFFF);\n
        }\n
\n
        var args = [row, 0];\n
        args.push.apply(args, lines);\n
        this.$lines.splice.apply(this.$lines, args);\n
\n
        var range = new Range(row, 0, row + lines.length, 0);\n
        var delta = {\n
            action: "insertLines",\n
            range: range,\n
            lines: lines\n
        };\n
        this._emit("change", { data: delta });\n
        return end || range.end;\n
    };\n
    this.insertNewLine = function(position) {\n
        position = this.$clipPosition(position);\n
        var line = this.$lines[position.row] || "";\n
\n
        this.$lines[position.row] = line.substring(0, position.column);\n
        this.$lines.splice(position.row + 1, 0, line.substring(position.column, line.length));\n
\n
        var end = {\n
            row : position.row + 1,\n
            column : 0\n
        };\n
\n
        var delta = {\n
            action: "insertText",\n
            range: Range.fromPoints(position, end),\n
            text: this.getNewLineCharacter()\n
        };\n
        this._emit("change", { data: delta });\n
\n
        return end;\n
    };\n
    this.insertInLine = function(position, text) {\n
        if (text.length == 0)\n
            return position;\n
\n
        var line = this.$lines[position.row] || "";\n
\n
        this.$lines[position.row] = line.substring(0, position.column) + text\n
                + line.substring(position.column);\n
\n
        var end = {\n
            row : position.row,\n
            column : position.column + text.length\n
        };\n
\n
        var delta = {\n
            action: "insertText",\n
            range: Range.fromPoints(position, end),\n
            text: text\n
        };\n
        this._emit("change", { data: delta });\n
\n
        return end;\n
    };\n
    this.remove = function(range) {\n
        if (!range instanceof Range)\n
            range = Range.fromPoints(range.start, range.end);\n
        range.start = this.$clipPosition(range.start);\n
        range.end = this.$clipPosition(range.end);\n
\n
        if (range.isEmpty())\n
            return range.start;\n
\n
        var firstRow = range.start.row;\n
        var lastRow = range.end.row;\n
\n
        if (range.isMultiLine()) {\n
            var firstFullRow = range.start.column == 0 ? firstRow : firstRow + 1;\n
            var lastFullRow = lastRow - 1;\n
\n
            if (range.end.column > 0)\n
                this.removeInLine(lastRow, 0, range.end.column);\n
\n
            if (lastFullRow >= firstFullRow)\n
                this._removeLines(firstFullRow, lastFullRow);\n
\n
            if (firstFullRow != firstRow) {\n
                this.removeInLine(firstRow, range.start.column, this.getLine(firstRow).length);\n
                this.removeNewLine(range.start.row);\n
            }\n
        }\n
        else {\n
            this.removeInLine(firstRow, range.start.column, range.end.column);\n
        }\n
        return range.start;\n
    };\n
    this.removeInLine = function(row, startColumn, endColumn) {\n
        if (startColumn == endColumn)\n
            return;\n
\n
        var range = new Range(row, startColumn, row, endColumn);\n
        var line = this.getLine(row);\n
        var removed = line.substring(startColumn, endColumn);\n
        var newLine = line.substring(0, startColumn) + line.substring(endColumn, line.length);\n
        this.$lines.splice(row, 1, newLine);\n
\n
        var delta = {\n
            action: "removeText",\n
            range: range,\n
            text: removed\n
        };\n
        this._emit("change", { data: delta });\n
        return range.start;\n
    };\n
    this.removeLines = function(firstRow, lastRow) {\n
        if (firstRow < 0 || lastRow >= this.getLength())\n
            return this.remove(new Range(firstRow, 0, lastRow + 1, 0));\n
        return this._removeLines(firstRow, lastRow);\n
    };\n
\n
    this._removeLines = function(firstRow, lastRow) {\n
        var range = new Range(firstRow, 0, lastRow + 1, 0);\n
        var removed = this.$lines.splice(firstRow, lastRow - firstRow + 1);\n
\n
        var delta = {\n
            action: "removeLines",\n
            range: range,\n
            nl: this.getNewLineCharacter(),\n
            lines: removed\n
        };\n
        this._emit("change", { data: delta });\n
        return removed;\n
    };\n
    this.removeNewLine = function(row) {\n
        var firstLine = this.getLine(row);\n
        var secondLine = this.getLine(row+1);\n
\n
        var range = new Range(row, firstLine.length, row+1, 0);\n
        var line = firstLine + secondLine;\n
\n
        this.$lines.splice(row, 2, line);\n
\n
        var delta = {\n
            action: "removeText",\n
            range: range,\n
            text: this.getNewLineCharacter()\n
        };\n
        this._emit("change", { data: delta });\n
    };\n
    this.replace = function(range, text) {\n
        if (!range instanceof Range)\n
            range = Range.fromPoints(range.start, range.end);\n
        if (text.length == 0 && range.isEmpty())\n
            return range.start;\n
        if (text == this.getTextRange(range))\n
            return range.end;\n
\n
        this.remove(range);\n
        if (text) {\n
            var end = this.insert(range.start, text);\n
        }\n
        else {\n
            end = range.start;\n
        }\n
\n
        return end;\n
    };\n
    this.applyDeltas = function(deltas) {\n
        for (var i=0; i<deltas.length; i++) {\n
            var delta = deltas[i];\n
            var range = Range.fromPoints(delta.range.start, delta.range.end);\n
\n
            if (delta.action == "insertLines")\n
                this.insertLines(range.start.row, delta.lines);\n
            else if (delta.action == "insertText")\n
                this.insert(range.start, delta.text);\n
            else if (delta.action == "removeLines")\n
                this._removeLines(range.start.row, range.end.row - 1);\n
            else if (delta.action == "removeText")\n
                this.remove(range);\n
        }\n
    };\n
    this.revertDeltas = function(deltas) {\n
        for (var i=deltas.length-1; i>=0; i--) {\n
            var delta = deltas[i];\n
\n
            var range = Range.fromPoints(delta.range.start, delta.range.end);\n
\n
            if (delta.action == "insertLines")\n
                this._removeLines(range.start.row, range.end.row - 1);\n
            else if (delta.action == "insertText")\n
                this.remove(range);\n
            else if (delta.action == "removeLines")\n
                this._insertLines(range.start.row, delta.lines);\n
            else if (delta.action == "removeText")\n
                this.insert(range.start, delta.text);\n
        }\n
    };\n
    this.indexToPosition = function(index, startRow) {\n
        var lines = this.$lines || this.getAllLines();\n
        var newlineLength = this.getNewLineCharacter().length;\n
        for (var i = startRow || 0, l = lines.length; i < l; i++) {\n
            index -= lines[i].length + newlineLength;\n
            if (index < 0)\n
                return {row: i, column: index + lines[i].length + newlineLength};\n
        }\n
        return {row: l-1, column: lines[l-1].length};\n
    };\n
    this.positionToIndex = function(pos, startRow) {\n
        var lines = this.$lines || this.getAllLines();\n
        var newlineLength = this.getNewLineCharacter().length;\n
        var index = 0;\n
        var row = Math.min(pos.row, lines.length);\n
        for (var i = startRow || 0; i < row; ++i)\n
            index += lines[i].length + newlineLength;\n
\n
        return index + pos.column;\n
    };\n
\n
}).call(Document.prototype);\n
\n
exports.Document = Document;\n
});\n
\n
define(\'ace/lib/event_emitter\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
\n
var EventEmitter = {};\n
var stopPropagation = function() { this.propagationStopped = true; };\n
var preventDefault = function() { this.defaultPrevented = true; };\n
\n
EventEmitter._emit =\n
EventEmitter._dispatchEvent = function(eventName, e) {\n
    this._eventRegistry || (this._eventRegistry = {});\n
    this._defaultHandlers || (this._defaultHandlers = {});\n
\n
    var listeners = this._eventRegistry[eventName] || [];\n
    var defaultHandler = this._defaultHandlers[eventName];\n
    if (!listeners.length && !defaultHandler)\n
        return;\n
\n
    if (typeof e != "object" || !e)\n
        e = {};\n
\n
    if (!e.type)\n
        e.type = eventName;\n
    if (!e.stopPropagation)\n
        e.stopPropagation = stopPropagation;\n
    if (!e.preventDefault)\n
        e.preventDefault = preventDefault;\n
\n
    listeners = listeners.slice();\n
    for (var i=0; i<listeners.length; i++) {\n
        listeners[i](e, this);\n
        if (e.propagationStopped)\n
            break;\n
    }\n
    \n
    if (defaultHandler && !e.defaultPrevented)\n
        return defaultHandler(e, this);\n
};\n
\n
\n
EventEmitter._signal = function(eventName, e) {\n
    var listeners = (this._eventRegistry || {})[eventName];\n
    if (!listeners)\n
        return;\n
    listeners = listeners.slice();\n
    for (var i=0; i<listeners.length; i++)\n
        listeners[i](e, this);\n
};\n
\n
EventEmitter.once = function(eventName, callback) {\n
    var _self = this;\n
    callback && this.addEventListener(eventName, function newCallback() {\n
        _self.removeEventListener(eventName, newCallback);\n
        callback.apply(null, arguments);\n
    });\n
};\n
\n
\n
EventEmitter.setDefaultHandler = function(eventName, callback) {\n
    var handlers = this._defaultHandlers\n
    if (!handlers)\n
        handlers = this._defaultHandlers = {_disabled_: {}};\n
    \n
    if (handlers[eventName]) {\n
        var old = handlers[eventName];\n
        var disabled = handlers._disabled_[eventName];\n
        if (!disabled)\n
            handlers._disabled_[eventName] = disabled = [];\n
        disabled.push(old);\n
        var i = disabled.indexOf(callback);\n
        if (i != -1) \n
            disabled.splice(i, 1);\n
    }\n
    handlers[eventName] = callback;\n
};\n
EventEmitter.removeDefaultHandler = function(eventName, callback) {\n
    var handlers = this._defaultHandlers\n
    if (!handlers)\n
        return;\n
    var disabled = handlers._disabled_[eventName];\n
    \n
    if (handlers[eventName] == callback) {\n
        var old = handlers[eventName];\n
        if (disabled)\n
            this.setDefaultHandler(eventName, disabled.pop());\n
    } else if (disabled) {\n
        var i = disabled.indexOf(callback);\n
        if (i != -1)\n
            disabled.splice(i, 1);\n
    }\n
};\n
\n
EventEmitter.on =\n
EventEmitter.addEventListener = function(eventName, callback, capturing) {\n
    this._eventRegistry = this._eventRegistry || {};\n
\n
    var listeners = this._eventRegistry[eventName];\n
    if (!listeners)\n
        listeners = this._eventRegistry[eventName] = [];\n
\n
    if (listeners.indexOf(callback) == -1)\n
        listeners[capturing ? "unshift" : "push"](callback);\n
    return callback;\n
};\n
\n
EventEmitter.off =\n
EventEmitter.removeListener =\n
EventEmitter.removeEventListener = function(eventName, callback) {\n
    this._eventRegistry = this._eventRegistry || {};\n
\n
    var listeners = this._eventRegistry[eventName];\n
    if (!listeners)\n
        return;\n
\n
    var index = listeners.indexOf(callback);\n
    if (index !== -1)\n
        listeners.splice(index, 1);\n
};\n
\n
EventEmitter.removeAllListeners = function(eventName) {\n
    if (this._eventRegistry) this._eventRegistry[eventName] = [];\n
};\n
\n
exports.EventEmitter = EventEmitter;\n
\n
});\n
\n
define(\'ace/range\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
var comparePoints = function(p1, p2) {\n
    return p1.row - p2.row || p1.column - p2.column;\n
};\n
var Range = function(startRow, startColumn, endRow, endColumn) {\n
    this.start = {\n
        row: startRow,\n
        column: startColumn\n
    };\n
\n
    this.end = {\n
        row: endRow,\n
        column: endColumn\n
    };\n
};\n
\n
(function() {\n
    this.isEqual = function(range) {\n
        return this.start.row === range.start.row &&\n
            this.end.row === range.end.row &&\n
            this.start.column === range.start.column &&\n
            this.end.column === range.end.column;\n
    };\n
    this.toString = function() {\n
        return ("Range: [" + this.start.row + "/" + this.start.column +\n
            "] -> [" + this.end.row + "/" + this.end.column + "]");\n
    };\n
\n
    this.contains = function(row, column) {\n
        return this.compare(row, column) == 0;\n
    };\n
    this.compareRange = function(range) {\n
        var cmp,\n
            end = range.end,\n
            start = range.start;\n
\n
        cmp = this.compare(end.row, end.column);\n
        if (cmp == 1) {\n
            cmp = this.compare(start.row, start.column);\n
            if (cmp == 1) {\n
                return 2;\n
            } else if (cmp == 0) {\n
                return 1;\n
            } else {\n
                return 0;\n
            }\n
        } else if (cmp == -1) {\n
            return -2;\n
        } else {\n
            cmp = this.compare(start.row, start.column);\n
            if (cmp == -1) {\n
                return -1;\n
            } else if (cmp == 1) {\n
                return 42;\n
            } else {\n
                return 0;\n
            }\n
        }\n
    };\n
    this.comparePoint = function(p) {\n
        return this.compare(p.row, p.column);\n
    };\n
    this.containsRange = function(range) {\n
        return this.comparePoint(range.start) == 0 && this.comparePoint(range.end) == 0;\n
    };\n
    this.intersects = function(range) {\n
        var cmp = this.compareRange(range);\n
        return (cmp == -1 || cmp == 0 || cmp == 1);\n
    };\n
    this.isEnd = function(row, column) {\n
        return this.end.row == row && this.end.column == column;\n
    };\n
    this.isStart = function(row, column) {\n
        return this.start.row == row && this.start.column == column;\n
    };\n
    this.setStart = function(row, column) {\n
        if (typeof row == "object") {\n
            this.start.column = row.column;\n
            this.start.row = row.row;\n
        } else {\n
            this.start.row = row;\n
            this.start.column = column;\n
        }\n
    };\n
    this.setEnd = function(row, column) {\n
        if (typeof row == "object") {\n
            this.end.column = row.column;\n
            this.end.row = row.row;\n
        } else {\n
            this.end.row = row;\n
            this.end.column = column;\n
        }\n
    };\n
    this.inside = function(row, column) {\n
        if (this.compare(row, column) == 0) {\n
            if (this.isEnd(row, column) || this.isStart(row, column)) {\n
                return false;\n
            } else {\n
                return true;\n
            }\n
        }\n
        return false;\n
    };\n
    this.insideStart = function(row, column) {\n
        if (this.compare(row, column) == 0) {\n
            if (this.isEnd(row, column)) {\n
                return false;\n
            } else {\n
                return true;\n
            }\n
        }\n
        return false;\n
    };\n
    this.insideEnd = function(row, column) {\n
        if (this.compare(row, column) == 0) {\n
            if (this.isStart(row, column)) {\n
                return false;\n
            } else {\n
                return true;\n
            }\n
        }\n
        return false;\n
    };\n
    this.compare = function(row, column) {\n
        if (!this.isMultiLine()) {\n
            if (row === this.start.row) {\n
                return column < this.start.column ? -1 : (column > this.end.column ? 1 : 0);\n
            };\n
        }\n
\n
        if (row < this.start.row)\n
            return -1;\n
\n
        if (row > this.end.row)\n
            return 1;\n
\n
        if (this.start.row === row)\n
            return column >= this.start.column ? 0 : -1;\n
\n
        if (this.end.row === row)\n
            return column <= this.end.column ? 0 : 1;\n
\n
        return 0;\n
    };\n
    this.compareStart = function(row, column) {\n
        if (this.start.row == row && this.start.column == column) {\n
            return -1;\n
        } else {\n
            return this.compare(row, column);\n
        }\n
    };\n
    this.compareEnd = function(row, column) {\n
        if (this.end.row == row && this.end.column == column) {\n
            return 1;\n
        } else {\n
            return this.compare(row, column);\n
        }\n
    };\n
    this.compareInside = function(row, column) {\n
        if (this.end.row == row && this.end.column == column) {\n
            return 1;\n
        } else if (this.start.row == row && this.start.column == column) {\n
            return -1;\n
        } else {\n
            return this.compare(row, column);\n
        }\n
    };\n
    this.clipRows = function(firstRow, lastRow) {\n
        if (this.end.row > lastRow)\n
            var end = {row: lastRow + 1, column: 0};\n
        else if (this.end.row < firstRow)\n
            var end = {row: firstRow, column: 0};\n
\n
        if (this.start.row > lastRow)\n
            var start = {row: lastRow + 1, column: 0};\n
        else if (this.start.row < firstRow)\n
            var start = {row: firstRow, column: 0};\n
\n
        return Range.fromPoints(start || this.start, end || this.end);\n
    };\n
    this.extend = function(row, column) {\n
        var cmp = this.compare(row, column);\n
\n
        if (cmp == 0)\n
            return this;\n
        else if (cmp == -1)\n
            var start = {row: row, column: column};\n
        else\n
            var end = {row: row, column: column};\n
\n
        return Range.fromPoints(start || this.start, end || this.end);\n
    };\n
\n
    this.isEmpty = function() {\n
        return (this.start.row === this.end.row && this.start.column === this.end.column);\n
    };\n
    this.isMultiLine = function() {\n
        return (this.start.row !== this.end.row);\n
    };\n
    this.clone = function() {\n
        return Range.fromPoints(this.start, this.end);\n
    };\n
    this.collapseRows = function() {\n
        if (this.end.column == 0)\n
            return new Range(this.start.row, 0, Math.max(this.start.row, this.end.row-1), 0)\n
        else\n
            return new Range(this.start.row, 0, this.end.row, 0)\n
    };\n
    this.toScreenRange = function(session) {\n
        var screenPosStart = session.documentToScreenPosition(this.start);\n
        var screenPosEnd = session.documentToScreenPosition(this.end);\n
\n
        return new Range(\n
            screenPosStart.row, screenPosStart.column,\n
            screenPosEnd.row, screenPosEnd.column\n
        );\n
    };\n
    this.moveBy = function(row, column) {\n
        this.start.row += row;\n
        this.start.column += column;\n
        this.end.row += row;\n
        this.end.column += column;\n
    };\n
\n
}).call(Range.prototype);\n
Range.fromPoints = function(start, end) {\n
    return new Range(start.row, start.column, end.row, end.column);\n
};\n
Range.comparePoints = comparePoints;\n
\n
Range.comparePoints = function(p1, p2) {\n
    return p1.row - p2.row || p1.column - p2.column;\n
};\n
\n
\n
exports.Range = Range;\n
});\n
\n
define(\'ace/anchor\', [\'require\', \'exports\', \'module\' , \'ace/lib/oop\', \'ace/lib/event_emitter\'], function(require, exports, module) {\n
\n
\n
var oop = require("./lib/oop");\n
var EventEmitter = require("./lib/event_emitter").EventEmitter;\n
\n
var Anchor = exports.Anchor = function(doc, row, column) {\n
    this.$onChange = this.onChange.bind(this);\n
    this.attach(doc);\n
    \n
    if (typeof column == "undefined")\n
        this.setPosition(row.row, row.column);\n
    else\n
        this.setPosition(row, column);\n
};\n
\n
(function() {\n
\n
    oop.implement(this, EventEmitter);\n
    this.getPosition = function() {\n
        return this.$clipPositionToDocument(this.row, this.column);\n
    };\n
    this.getDocument = function() {\n
        return this.document;\n
    };\n
    this.$insertRight = false;\n
    this.onChange = function(e) {\n
        var delta = e.data;\n
        var range = delta.range;\n
\n
        if (range.start.row == range.end.row && range.start.row != this.row)\n
            return;\n
\n
        if (range.start.row > this.row)\n
            return;\n
\n
        if (range.start.row == this.row && range.start.column > this.column)\n
            return;\n
\n
        var row = this.row;\n
        var column = this.column;\n
        var start = range.start;\n
        var end = range.end;\n
\n
        if (delta.action === "insertText") {\n
            if (start.row === row && start.column <= column) {\n
                if (start.column === column && this.$insertRight) {\n
                } else if (start.row === end.row) {\n
                    column += end.column - start.column;\n
                } else {\n
                    column -= start.column;\n
                    row += end.row - start.row;\n
                }\n
            } else if (start.row !== end.row && start.row < row) {\n
                row += end.row - start.row;\n
            }\n
        } else if (delta.action === "insertLines") {\n
            if (start.row <= row) {\n
                row += end.row - start.row;\n
            }\n
        } else if (delta.action === "removeText") {\n
            if (start.row === row && start.column < column) {\n
                if (end.column >= column)\n
                    column = start.column;\n
                else\n
                    column = Math.max(0, column - (end.column - start.column));\n
\n
            } else if (start.row !== end.row && start.row < row) {\n
                if (end.row === row)\n
                    column = Math.max(0, column - end.column) + start.column;\n
                row -= (end.row - start.row);\n
            } else if (end.row === row) {\n
                row -= end.row - start.row;\n
                column = Math.max(0, column - end.column) + start.column;\n
            }\n
        } else if (delta.action == "removeLines") {\n
            if (start.row <= row) {\n
                if (end.row <= row)\n
                    row -= end.row - start.row;\n
                else {\n
                    row = start.row;\n
                    column = 0;\n
                }\n
            }\n
        }\n
\n
        this.setPosition(row, column, true);\n
    };\n
    this.setPosition = function(row, column, noClip) {\n
        var pos;\n
        if (noClip) {\n
            pos = {\n
                row: row,\n
                column: column\n
            };\n
        } else {\n
            pos = this.$clipPositionToDocument(row, column);\n
        }\n
\n
        if (this.row == pos.row && this.column == pos.column)\n
            return;\n
\n
        var old = {\n
            row: this.row,\n
            column: this.column\n
        };\n
\n
        this.row = pos.row;\n
        this.column = pos.column;\n
        this._emit("change", {\n
            old: old,\n
            value: pos\n
        });\n
    };\n
    this.detach = function() {\n
        this.document.removeEventListener("change", this.$onChange);\n
    };\n
    this.attach = function(doc) {\n
        this.document = doc || this.document;\n
        this.document.on("change", this.$onChange);\n
    };\n
    this.$clipPositionToDocument = function(row, column) {\n
        var pos = {};\n
\n
        if (row >= this.document.getLength()) {\n
            pos.row = Math.max(0, this.document.getLength() - 1);\n
            pos.column = this.document.getLine(pos.row).length;\n
        }\n
        else if (row < 0) {\n
            pos.row = 0;\n
            pos.column = 0;\n
        }\n
        else {\n
            pos.row = row;\n
            pos.column = Math.min(this.document.getLine(pos.row).length, Math.max(0, column));\n
        }\n
\n
        if (column < 0)\n
            pos.column = 0;\n
\n
        return pos;\n
    };\n
\n
}).call(Anchor.prototype);\n
\n
});\n
\n
define(\'ace/lib/lang\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
\n
exports.stringReverse = function(string) {\n
    return string.split("").reverse().join("");\n
};\n
\n
exports.stringRepeat = function (string, count) {\n
    var result = \'\';\n
    while (count > 0) {\n
        if (count & 1)\n
            result += string;\n
\n
        if (count >>= 1)\n
            string += string;\n
    }\n
    return result;\n
};\n
\n
var trimBeginRegexp = /^\\s\\s*/;\n
var trimEndRegexp = /\\s\\s*$/;\n
\n
exports.stringTrimLeft = function (string) {\n
    return string.replace(trimBeginRegexp, \'\');\n
};\n
\n
exports.stringTrimRight = function (string) {\n
    return string.replace(trimEndRegexp, \'\');\n
};\n
\n
exports.copyObject = function(obj) {\n
    var copy = {};\n
    for (var key in obj) {\n
        copy[key] = obj[key];\n
    }\n
    return copy;\n
};\n
\n
exports.copyArray = function(array){\n
    var copy = [];\n
    for (var i=0, l=array.length; i<l; i++) {\n
        if (array[i] && typeof array[i] == "object")\n
            copy[i] = this.copyObject( array[i] );\n
        else \n
            copy[i] = array[i];\n
    }\n
    return copy;\n
};\n
\n
exports.deepCopy = function (obj) {\n
    if (typeof obj != "object") {\n
        return obj;\n
    }\n
    \n
    var copy = obj.constructor();\n
    for (var key in obj) {\n
        if (typeof obj[key] == "object") {\n
            copy[key] = this.deepCopy(obj[key]);\n
        } else {\n
            copy[key] = obj[key];\n
        }\n
    }\n
    return copy;\n
};\n
\n
exports.arrayToMap = function(arr) {\n
    var map = {};\n
    for (var i=0; i<arr.length; i++) {\n
        map[arr[i]] = 1;\n
    }\n
    return map;\n
\n
};\n
\n
exports.createMap = function(props) {\n
    var map = Object.create(null);\n
    for (var i in props) {\n
        map[i] = props[i];\n
    }\n
    return map;\n
};\n
exports.arrayRemove = function(array, value) {\n
  for (var i = 0; i <= array.length; i++) {\n
    if (value === array[i]) {\n
      array.splice(i, 1);\n
    }\n
  }\n
};\n
\n
exports.escapeRegExp = function(str) {\n
    return str.replace(/([.*+?^${}()|[\\]\\/\\\\])/g, \'\\\\$1\');\n
};\n
\n
exports.escapeHTML = function(str) {\n
    return str.replace(/&/g, "&#38;").replace(/"/g, "&#34;").replace(/\'/g, "&#39;").replace(/</g, "&#60;");\n
};\n
\n
exports.getMatchOffsets = function(string, regExp) {\n
    var matches = [];\n
\n
    string.replace(regExp, function(str) {\n
        matches.push({\n
            offset: arguments[arguments.length-2],\n
            length: str.length\n
        });\n
    });\n
\n
    return matches;\n
};\n
exports.deferredCall = function(fcn) {\n
\n
    var timer = null;\n
    var callback = function() {\n
        timer = null;\n
        fcn();\n
    };\n
\n
    var deferred = function(timeout) {\n
        deferred.cancel();\n
        timer = setTimeout(callback, timeout || 0);\n
        return deferred;\n
    };\n
\n
    deferred.schedule = deferred;\n
\n
    deferred.call = function() {\n
        this.cancel();\n
        fcn();\n
        return deferred;\n
    };\n
\n
    deferred.cancel = function() {\n
        clearTimeout(timer);\n
        timer = null;\n
        return deferred;\n
    };\n
\n
    return deferred;\n
};\n
\n
\n
exports.delayedCall = function(fcn, defaultTimeout) {\n
    var timer = null;\n
    var callback = function() {\n
        timer = null;\n
        fcn();\n
    };\n
\n
    var _self = function(timeout) {\n
        timer && clearTimeout(timer);\n
        timer = setTimeout(callback, timeout || defaultTimeout);\n
    };\n
\n
    _self.delay = _self;\n
    _self.schedule = function(timeout) {\n
        if (timer == null)\n
            timer = setTimeout(callback, timeout || 0);\n
    };\n
\n
    _self.call = function() {\n
        this.cancel();\n
        fcn();\n
    };\n
\n
    _self.cancel = function() {\n
        timer && clearTimeout(timer);\n
        timer = null;\n
    };\n
\n
    _self.isPending = function() {\n
        return timer;\n
    };\n
\n
    return _self;\n
};\n
});\n
\n
define(\'ace/mode/coffee/coffee-script\', [\'require\', \'exports\', \'module\' , \'ace/mode/coffee/lexer\', \'ace/mode/coffee/parser\', \'ace/mode/coffee/nodes\'], function(require, exports, module) {\n
\n
    var Lexer = require("./lexer").Lexer;\n
    var parser = require("./parser");\n
\n
    var lexer = new Lexer();\n
    parser.lexer = {\n
        lex: function() {\n
            var tag, token;\n
            token = this.tokens[this.pos++];\n
            if (token) {\n
                tag = token[0], this.yytext = token[1], this.yylloc = token[2];\n
                this.yylineno = this.yylloc.first_line;\n
            } else {\n
                tag = \'\';\n
            }\n
            return tag;\n
        },\n
        setInput: function(tokens) {\n
            this.tokens = tokens;\n
            return this.pos = 0;\n
        },\n
        upcomingInput: function() {\n
            return "";\n
        }\n
    };\n
    parser.yy = require(\'./nodes\');\n
\n
    exports.parse = function(code) {\n
        return parser.parse(lexer.tokenize(code));\n
    };\n
});\n
\n
define(\'ace/mode/coffee/lexer\', [\'require\', \'exports\', \'module\' , \'ace/mode/coffee/rewriter\', \'ace/mode/coffee/helpers\'], function(require, exports, module) {\n
\n
  var BOM, BOOL, CALLABLE, CODE, COFFEE_ALIASES, COFFEE_ALIAS_MAP, COFFEE_KEYWORDS, COMMENT, COMPARE, COMPOUND_ASSIGN, HEREDOC, HEREDOC_ILLEGAL, HEREDOC_INDENT, HEREGEX, HEREGEX_OMIT, IDENTIFIER, INDEXABLE, INVERSES, JSTOKEN, JS_FORBIDDEN, JS_KEYWORDS, LINE_BREAK, LINE_CONTINUER, LOGIC, Lexer, MATH, MULTILINER, MULTI_DENT, NOT_REGEX, NOT_SPACED_REGEX, NUMBER, OPERATOR, REGEX, RELATION, RESERVED, Rewriter, SHIFT, SIMPLESTR, STRICT_PROSCRIBED, TRAILING_SPACES, UNARY, WHITESPACE, compact, count, invertLiterate, key, last, locationDataToString, repeat, starts, throwSyntaxError, _ref, _ref1,\n
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };\n
\n
  _ref = require(\'./rewriter\'), Rewriter = _ref.Rewriter, INVERSES = _ref.INVERSES;\n
\n
  _ref1 = require(\'./helpers\'), count = _ref1.count, starts = _ref1.starts, compact = _ref1.compact, last = _ref1.last, repeat = _ref1.repeat, invertLiterate = _ref1.invertLiterate, locationDataToString = _ref1.locationDataToString, throwSyntaxError = _ref1.throwSyntaxError;\n
\n
  exports.Lexer = Lexer = (function() {\n
    function Lexer() {}\n
\n
    Lexer.prototype.tokenize = function(code, opts) {\n
      var consumed, i, tag, _ref2;\n
      if (opts == null) {\n
        opts = {};\n
      }\n
      this.literate = opts.literate;\n
      this.indent = 0;\n
      this.baseIndent = 0;\n
      this.indebt = 0;\n
      this.outdebt = 0;\n
      this.indents = [];\n
      this.ends = [];\n
      this.tokens = [];\n
      this.chunkLine = opts.line || 0;\n
      this.chunkColumn = opts.column || 0;\n
      code = this.clean(code);\n
      i = 0;\n
      while (this.chunk = code.slice(i)) {\n
        consumed = this.identifierToken() || this.commentToken() || this.whitespaceToken() || this.lineToken() || this.heredocToken() || this.stringToken() || this.numberToken() || this.regexToken() || this.jsToken() || this.literalToken();\n
        _ref2 = this.getLineAndColumnFromChunk(consumed), this.chunkLine = _ref2[0], this.chunkColumn = _ref2[1];\n
        i += consumed;\n
      }\n
      this.closeIndentation();\n
      if (tag = this.ends.pop()) {\n
        this.error("missing " + tag);\n
      }\n
      if (opts.rewrite === false) {\n
        return this.tokens;\n
      }\n
      return (new Rewriter).rewrite(this.tokens);\n
    };\n
\n
    Lexer.prototype.clean = function(code) {\n
      if (code.charCodeAt(0) === BOM) {\n
        code = code.slice(1);\n
      }\n
      code = code.replace(/\\r/g, \'\').replace(TRAILING_SPACES, \'\');\n
      if (WHITESPACE.test(code)) {\n
        code = "\\n" + code;\n
        this.chunkLine--;\n
      }\n
      if (this.literate) {\n
        code = invertLiterate(code);\n
      }\n
      return code;\n
    };\n
\n
    Lexer.prototype.identifierToken = function() {\n
      var colon, colonOffset, forcedIdentifier, id, idLength, input, match, poppedToken, prev, tag, tagToken, _ref2, _ref3, _ref4;\n
      if (!(match = IDENTIFIER.exec(this.chunk))) {\n
        return 0;\n
      }\n
      input = match[0], id = match[1], colon = match[2];\n
      idLength = id.length;\n
      poppedToken = void 0;\n
      if (id === \'own\' && this.tag() === \'FOR\') {\n
        this.token(\'OWN\', id);\n
        return id.length;\n
      }\n
      forcedIdentifier = colon || (prev = last(this.tokens)) && (((_ref2 = prev[0]) === \'.\' || _ref2 === \'?.\' || _ref2 === \'::\' || _ref2 === \'?::\') || !prev.spaced && prev[0] === \'@\');\n
      tag = \'IDENTIFIER\';\n
      if (!forcedIdentifier && (__indexOf.call(JS_KEYWORDS, id) >= 0 || __indexOf.call(COFFEE_KEYWORDS, id) >= 0)) {\n
        tag = id.toUpperCase();\n
        if (tag === \'WHEN\' && (_ref3 = this.tag(), __indexOf.call(LINE_BREAK, _ref3) >= 0)) {\n
          tag = \'LEADING_WHEN\';\n
        } else if (tag === \'FOR\') {\n
          this.seenFor = true;\n
        } else if (tag === \'UNLESS\') {\n
          tag = \'IF\';\n
        } else if (__indexOf.call(UNARY, tag) >= 0) {\n
          tag = \'UNARY\';\n
        } else if (__indexOf.call(RELATION, tag) >= 0) {\n
          if (tag !== \'INSTANCEOF\' && this.seenFor) {\n
            tag = \'FOR\' + tag;\n
            this.seenFor = false;\n
          } else {\n
            tag = \'RELATION\';\n
            if (this.value() === \'!\') {\n
              poppedToken = this.tokens.pop();\n
              id = \'!\' + id;\n
            }\n
          }\n
        }\n
      }\n
      if (__indexOf.call(JS_FORBIDDEN, id) >= 0) {\n
        if (forcedIdentifier) {\n
          tag = \'IDENTIFIER\';\n
          id = new String(id);\n
          id.reserved = true;\n
        } else if (__indexOf.call(RESERVED, id) >= 0) {\n
          this.error("reserved word \\"" + id + "\\"");\n
        }\n
      }\n
      if (!forcedIdentifier) {\n
        if (__indexOf.call(COFFEE_ALIASES, id) >= 0) {\n
          id = COFFEE_ALIAS_MAP[id];\n
        }\n
        tag = (function() {\n
          switch (id) {\n
            case \'!\':\n
              return \'UNARY\';\n
            case \'==\':\n
            case \'!=\':\n
              return \'COMPARE\';\n
            case \'&&\':\n
            case \'||\':\n
              return \'LOGIC\';\n
            case \'true\':\n
            case \'false\':\n
              return \'BOOL\';\n
            case \'break\':\n
            case \'continue\':\n
              return \'STATEMENT\';\n
            default:\n
              return tag;\n
          }\n
        })();\n
      }\n
      tagToken = this.token(tag, id, 0, idLength);\n
      if (poppedToken) {\n
        _ref4 = [poppedToken[2].first_line, poppedToken[2].first_column], tagToken[2].first_line = _ref4[0], tagToken[2].first_column = _ref4[1];\n
      }\n
      if (colon) {\n
        colonOffset = input.lastIndexOf(\':\');\n
        this.token(\':\', \':\', colonOffset, colon.length);\n
      }\n
      return input.length;\n
    };\n
\n
    Lexer.prototype.numberToken = function() {\n
      var binaryLiteral, lexedLength, match, number, octalLiteral;\n
      if (!(match = NUMBER.exec(this.chunk))) {\n
        return 0;\n
      }\n
      number = match[0];\n
      if (/^0[BOX]/.test(number)) {\n
        this.error("radix prefix \'" + number + "\' must be lowercase");\n
      } else if (/E/.test(number) && !/^0x/.test(number)) {\n
        this.error("exponential notation \'" + number + "\' must be indicated with a lowercase \'e\'");\n
      } else if (/^0\\d*[89]/.test(number)) {\n
        this.error("decimal literal \'" + number + "\' must not be prefixed with \'0\'");\n
      } else if (/^0\\d+/.test(number)) {\n
        this.error("octal literal \'" + number + "\' must be prefixed with \'0o\'");\n
      }\n
      lexedLength = number.length;\n
      if (octalLiteral = /^0o([0-7]+)/.exec(number)) {\n
        number = \'0x\' + parseInt(octalLiteral[1], 8).toString(16);\n
      }\n
      if (binaryLiteral = /^0b([01]+)/.exec(number)) {\n
        number = \'0x\' + parseInt(binaryLiteral[1], 2).toString(16);\n
      }\n
      this.token(\'NUMBER\', number, 0, lexedLength);\n
      return lexedLength;\n
    };\n
\n
    Lexer.prototype.stringToken = function() {\n
      var match, octalEsc, string;\n
      switch (this.chunk.charAt(0)) {\n
        case "\'":\n
          if (!(match = SIMPLESTR.exec(this.chunk))) {\n
            return 0;\n
          }\n
          string = match[0];\n
          this.token(\'STRING\', string.replace(MULTILINER, \'\\\\\\n\'), 0, string.length);\n
          break;\n
        case \'"\':\n
          if (!(string = this.balancedString(this.chunk, \'"\'))) {\n
            return 0;\n
          }\n
          if (0 < string.indexOf(\'#{\', 1)) {\n
            this.interpolateString(string.slice(1, -1), {\n
              strOffset: 1,\n
              lexedLength: string.length\n
            });\n
          } else {\n
            this.token(\'STRING\', this.escapeLines(string, 0, string.length));\n
          }\n
          break;\n
        default:\n
          return 0;\n
      }\n
      if (octalEsc = /^(?:\\\\.|[^\\\\])*\\\\(?:0[0-7]|[1-7])/.test(string)) {\n
        this.error("octal escape sequences " + string + " are not allowed");\n
      }\n
      return string.length;\n
    };\n
\n
    Lexer.prototype.heredocToken = function() {\n
      var doc, heredoc, match, quote;\n
      if (!(match = HEREDOC.exec(this.chunk))) {\n
        return 0;\n
      }\n
      heredoc = match[0];\n
      quote = heredoc.charAt(0);\n
      doc = this.sanitizeHeredoc(match[2], {\n
        quote: quote,\n
        indent: null\n
      });\n
      if (quote === \'"\' && 0 <= doc.indexOf(\'#{\')) {\n
        this.interpolateString(doc, {\n
          heredoc: true,\n
          strOffset: 3,\n
          lexedLength: heredoc.length\n
        });\n
      } else {\n
        this.token(\'STRING\', this.makeString(doc, quote, true), 0, heredoc.length);\n
      }\n
      return heredoc.length;\n
    };\n
\n
    Lexer.prototype.commentToken = function() {\n
      var comment, here, match;\n
      if (!(match = this.chunk.match(COMMENT))) {\n
        return 0;\n
      }\n
      comment = match[0], here = match[1];\n
      if (here) {\n
        this.token(\'HERECOMMENT\', this.sanitizeHeredoc(here, {\n
          herecomment: true,\n
          indent: repeat(\' \', this.indent)\n
        }), 0, comment.length);\n
      }\n
      return comment.length;\n
    };\n
\n
    Lexer.prototype.jsToken = function() {\n
      var match, script;\n
      if (!(this.chunk.charAt(0) === \'`\' && (match = JSTOKEN.exec(this.chunk)))) {\n
        return 0;\n
      }\n
      this.token(\'JS\', (script = match[0]).slice(1, -1), 0, script.length);\n
      return script.length;\n
    };\n
\n
    Lexer.prototype.regexToken = function() {\n
      var flags, length, match, prev, regex, _ref2, _ref3;\n
      if (this.chunk.charAt(0) !== \'/\') {\n
        return 0;\n
      }\n
      if (match = HEREGEX.exec(this.chunk)) {\n
        length = this.heregexToken(match);\n
        return length;\n
      }\n
      prev = last(this.tokens);\n
      if (prev && (_ref2 = prev[0], __indexOf.call((prev.spaced ? NOT_REGEX : NOT_SPACED_REGEX), _ref2) >= 0)) {\n
        return 0;\n
      }\n
      if (!(match = REGEX.exec(this.chunk))) {\n
        return 0;\n
      }\n
      _ref3 = match, match = _ref3[0], regex = _ref3[1], flags = _ref3[2];\n
      if (regex.slice(0, 2) === \'/*\') {\n
        this.error(\'regular expressions cannot begin with `*`\');\n
      }\n
      if (regex === \'//\') {\n
        regex = \'/(?:)/\';\n
      }\n
      this.token(\'REGEX\', "" + regex + flags, 0, match.length);\n
      return match.length;\n
    };\n
\n
    Lexer.prototype.heregexToken = function(match) {\n
      var body, flags, flagsOffset, heregex, plusToken, prev, re, tag, token, tokens, value, _i, _len, _ref2, _ref3, _ref4;\n
      heregex = match[0], body = match[1], flags = match[2];\n
      if (0 > body.indexOf(\'#{\')) {\n
        re = body.replace(HEREGEX_OMIT, \'\').replace(/\\//g, \'\\\\/\');\n
        if (re.match(/^\\*/)) {\n
          this.error(\'regular expressions cannot begin with `*`\');\n
        }\n
        this.token(\'REGEX\', "/" + (re || \'(?:)\') + "/" + flags, 0, heregex.length);\n
        return heregex.length;\n
      }\n
      this.token(\'IDENTIFIER\', \'RegExp\', 0, 0);\n
      this.token(\'CALL_START\', \'(\', 0, 0);\n
      tokens = [];\n
      _ref2 = this.interpolateString(body, {\n
        regex: true\n
      });\n
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {\n
        token = _ref2[_i];\n
        tag = token[0], value = token[1];\n
        if (tag === \'TOKENS\') {\n
          tokens.push.apply(tokens, value);\n
        } else if (tag === \'NEOSTRING\') {\n
          if (!(value = value.replace(HEREGEX_OMIT, \'\'))) {\n
            continue;\n
          }\n
          value = value.replace(/\\\\/g, \'\\\\\\\\\');\n
          token[0] = \'STRING\';\n
          token[1] = this.makeString(value, \'"\', true);\n
          tokens.push(token);\n
        } else {\n
          this.error("Unexpected " + tag);\n
        }\n
        prev = last(this.tokens);\n
        plusToken = [\'+\', \'+\'];\n
        plusToken[2] = prev[2];\n
        tokens.push(plusToken);\n
      }\n
      tokens.pop();\n
      if (((_ref3 = tokens[0]) != null ? _ref3[0] : void 0) !== \'STRING\') {\n
        this.token(\'STRING\', \'""\', 0, 0);\n
        this.token(\'+\', \'+\', 0, 0);\n
      }\n
      (_ref4 = this.tokens).push.apply(_ref4, tokens);\n
      if (flags) {\n
        flagsOffset = heregex.lastIndexOf(flags);\n
        this.token(\',\', \',\', flagsOffset, 0);\n
        this.token(\'STRING\', \'"\' + flags + \'"\', flagsOffset, flags.length);\n
      }\n
      this.token(\')\', \')\', heregex.length - 1, 0);\n
      return heregex.length;\n
    };\n
\n
    Lexer.prototype.lineToken = function() {\n
      var diff, indent, match, noNewlines, size;\n
      if (!(match = MULTI_DENT.exec(this.chunk))) {\n
        return 0;\n
      }\n
      indent = match[0];\n
      this.seenFor = false;\n
      size = indent.length - 1 - indent.lastIndexOf(\'\\n\');\n
      noNewlines = this.unfinished();\n
      if (size - this.indebt === this.indent) {\n
        if (noNewlines) {\n
          this.suppressNewlines();\n
        } else {\n
          this.newlineToken(0);\n
        }\n
        return indent.length;\n
      }\n
      if (size > this.indent) {\n
        if (noNewlines) {\n
          this.indebt = size - this.indent;\n
          this.suppressNewlines();\n
          return indent.length;\n
        }\n
        if (!this.tokens.length) {\n
          this.baseIndent = this.indent = size;\n
          return indent.length;\n
        }\n
        diff = size - this.indent + this.outdebt;\n
        this.token(\'INDENT\', diff, indent.length - size, size);\n
        this.indents.push(diff);\n
        this.ends.push(\'OUTDENT\');\n
        this.outdebt = this.indebt = 0;\n
      } else if (size < this.baseIndent) {\n
        this.error(\'missing indentation\', indent.length);\n
      } else {\n
        this.indebt = 0;\n
        this.outdentToken(this.indent - size, noNewlines, indent.length);\n
      }\n
      this.indent = size;\n
      return indent.length;\n
    };\n
\n
    Lexer.prototype.outdentToken = function(moveOut, noNewlines, outdentLength) {\n
      var dent, len;\n
      while (moveOut > 0) {\n
        len = this.indents.length - 1;\n
        if (this.indents[len] === void 0) {\n
          moveOut = 0;\n
        } else if (this.indents[len] === this.outdebt) {\n
          moveOut -= this.outdebt;\n
          this.outdebt = 0;\n
        } else if (this.indents[len] < this.outdebt) {\n
          this.outdebt -= this.indents[len];\n
          moveOut -= this.indents[len];\n
        } else {\n
          dent = this.indents.pop() + this.outdebt;\n
          moveOut -= dent;\n
          this.outdebt = 0;\n
          this.pair(\'OUTDENT\');\n
          this.token(\'OUTDENT\', dent, 0, outdentLength);\n
        }\n
      }\n
      if (dent) {\n
        this.outdebt -= moveOut;\n
      }\n
      while (this.value() === \';\') {\n
        this.tokens.pop();\n
      }\n
      if (!(this.tag() === \'TERMINATOR\' || noNewlines)) {\n
        this.token(\'TERMINATOR\', \'\\n\', outdentLength, 0);\n
      }\n
      return this;\n
    };\n
\n
    Lexer.prototype.whitespaceToken = function() {\n
      var match, nline, prev;\n
      if (!((match = WHITESPACE.exec(this.chunk)) || (nline = this.chunk.charAt(0) === \'\\n\'))) {\n
        return 0;\n
      }\n
      prev = last(this.tokens);\n
      if (prev) {\n
        prev[match ? \'spaced\' : \'newLine\'] = true;\n
      }\n
      if (match) {\n
        return match[0].length;\n
      } else {\n
        return 0;\n
      }\n
    };\n
\n
    Lexer.prototype.newlineToken = function(offset) {\n
      while (this.value() === \';\') {\n
        this.tokens.pop();\n
      }\n
      if (this.tag() !== \'TERMINATOR\') {\n
        this.token(\'TERMINATOR\', \'\\n\', offset, 0);\n
      }\n
      return this;\n
    };\n
\n
    Lexer.prototype.suppressNewlines = function() {\n
      if (this.value() === \'\\\\\') {\n
        this.tokens.pop();\n
      }\n
      return this;\n
    };\n
\n
    Lexer.prototype.literalToken = function() {\n
      var match, prev, tag, value, _ref2, _ref3, _ref4, _ref5;\n
      if (match = OPERATOR.exec(t

]]></string> </value>
        </item>
        <item>
            <key> <string>next</string> </key>
            <value>
              <persistent> <string encoding="base64">AAAAAAAAAAM=</string> </persistent>
            </value>
        </item>
      </dictionary>
    </pickle>
  </record>
  <record id="3" aka="AAAAAAAAAAM=">
    <pickle>
      <global name="Pdata" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

his.chunk)) {\n
        value = match[0];\n
        if (CODE.test(value)) {\n
          this.tagParameters();\n
        }\n
      } else {\n
        value = this.chunk.charAt(0);\n
      }\n
      tag = value;\n
      prev = last(this.tokens);\n
      if (value === \'=\' && prev) {\n
        if (!prev[1].reserved && (_ref2 = prev[1], __indexOf.call(JS_FORBIDDEN, _ref2) >= 0)) {\n
          this.error("reserved word \\"" + (this.value()) + "\\" can\'t be assigned");\n
        }\n
        if ((_ref3 = prev[1]) === \'||\' || _ref3 === \'&&\') {\n
          prev[0] = \'COMPOUND_ASSIGN\';\n
          prev[1] += \'=\';\n
          return value.length;\n
        }\n
      }\n
      if (value === \';\') {\n
        this.seenFor = false;\n
        tag = \'TERMINATOR\';\n
      } else if (__indexOf.call(MATH, value) >= 0) {\n
        tag = \'MATH\';\n
      } else if (__indexOf.call(COMPARE, value) >= 0) {\n
        tag = \'COMPARE\';\n
      } else if (__indexOf.call(COMPOUND_ASSIGN, value) >= 0) {\n
        tag = \'COMPOUND_ASSIGN\';\n
      } else if (__indexOf.call(UNARY, value) >= 0) {\n
        tag = \'UNARY\';\n
      } else if (__indexOf.call(SHIFT, value) >= 0) {\n
        tag = \'SHIFT\';\n
      } else if (__indexOf.call(LOGIC, value) >= 0 || value === \'?\' && (prev != null ? prev.spaced : void 0)) {\n
        tag = \'LOGIC\';\n
      } else if (prev && !prev.spaced) {\n
        if (value === \'(\' && (_ref4 = prev[0], __indexOf.call(CALLABLE, _ref4) >= 0)) {\n
          if (prev[0] === \'?\') {\n
            prev[0] = \'FUNC_EXIST\';\n
          }\n
          tag = \'CALL_START\';\n
        } else if (value === \'[\' && (_ref5 = prev[0], __indexOf.call(INDEXABLE, _ref5) >= 0)) {\n
          tag = \'INDEX_START\';\n
          switch (prev[0]) {\n
            case \'?\':\n
              prev[0] = \'INDEX_SOAK\';\n
          }\n
        }\n
      }\n
      switch (value) {\n
        case \'(\':\n
        case \'{\':\n
        case \'[\':\n
          this.ends.push(INVERSES[value]);\n
          break;\n
        case \')\':\n
        case \'}\':\n
        case \']\':\n
          this.pair(value);\n
      }\n
      this.token(tag, value);\n
      return value.length;\n
    };\n
\n
    Lexer.prototype.sanitizeHeredoc = function(doc, options) {\n
      var attempt, herecomment, indent, match, _ref2;\n
      indent = options.indent, herecomment = options.herecomment;\n
      if (herecomment) {\n
        if (HEREDOC_ILLEGAL.test(doc)) {\n
          this.error("block comment cannot contain \\"*/\\", starting");\n
        }\n
        if (doc.indexOf(\'\\n\') < 0) {\n
          return doc;\n
        }\n
      } else {\n
        while (match = HEREDOC_INDENT.exec(doc)) {\n
          attempt = match[1];\n
          if (indent === null || (0 < (_ref2 = attempt.length) && _ref2 < indent.length)) {\n
            indent = attempt;\n
          }\n
        }\n
      }\n
      if (indent) {\n
        doc = doc.replace(RegExp("\\\\n" + indent, "g"), \'\\n\');\n
      }\n
      if (!herecomment) {\n
        doc = doc.replace(/^\\n/, \'\');\n
      }\n
      return doc;\n
    };\n
\n
    Lexer.prototype.tagParameters = function() {\n
      var i, stack, tok, tokens;\n
      if (this.tag() !== \')\') {\n
        return this;\n
      }\n
      stack = [];\n
      tokens = this.tokens;\n
      i = tokens.length;\n
      tokens[--i][0] = \'PARAM_END\';\n
      while (tok = tokens[--i]) {\n
        switch (tok[0]) {\n
          case \')\':\n
            stack.push(tok);\n
            break;\n
          case \'(\':\n
          case \'CALL_START\':\n
            if (stack.length) {\n
              stack.pop();\n
            } else if (tok[0] === \'(\') {\n
              tok[0] = \'PARAM_START\';\n
              return this;\n
            } else {\n
              return this;\n
            }\n
        }\n
      }\n
      return this;\n
    };\n
\n
    Lexer.prototype.closeIndentation = function() {\n
      return this.outdentToken(this.indent);\n
    };\n
\n
    Lexer.prototype.balancedString = function(str, end) {\n
      var continueCount, i, letter, match, prev, stack, _i, _ref2;\n
      continueCount = 0;\n
      stack = [end];\n
      for (i = _i = 1, _ref2 = str.length; 1 <= _ref2 ? _i < _ref2 : _i > _ref2; i = 1 <= _ref2 ? ++_i : --_i) {\n
        if (continueCount) {\n
          --continueCount;\n
          continue;\n
        }\n
        switch (letter = str.charAt(i)) {\n
          case \'\\\\\':\n
            ++continueCount;\n
            continue;\n
          case end:\n
            stack.pop();\n
            if (!stack.length) {\n
              return str.slice(0, +i + 1 || 9e9);\n
            }\n
            end = stack[stack.length - 1];\n
            continue;\n
        }\n
        if (end === \'}\' && (letter === \'"\' || letter === "\'")) {\n
          stack.push(end = letter);\n
        } else if (end === \'}\' && letter === \'/\' && (match = HEREGEX.exec(str.slice(i)) || REGEX.exec(str.slice(i)))) {\n
          continueCount += match[0].length - 1;\n
        } else if (end === \'}\' && letter === \'{\') {\n
          stack.push(end = \'}\');\n
        } else if (end === \'"\' && prev === \'#\' && letter === \'{\') {\n
          stack.push(end = \'}\');\n
        }\n
        prev = letter;\n
      }\n
      return this.error("missing " + (stack.pop()) + ", starting");\n
    };\n
\n
    Lexer.prototype.interpolateString = function(str, options) {\n
      var column, expr, heredoc, i, inner, interpolated, len, letter, lexedLength, line, locationToken, nested, offsetInChunk, pi, plusToken, popped, regex, rparen, strOffset, tag, token, tokens, value, _i, _len, _ref2, _ref3, _ref4;\n
      if (options == null) {\n
        options = {};\n
      }\n
      heredoc = options.heredoc, regex = options.regex, offsetInChunk = options.offsetInChunk, strOffset = options.strOffset, lexedLength = options.lexedLength;\n
      offsetInChunk = offsetInChunk || 0;\n
      strOffset = strOffset || 0;\n
      lexedLength = lexedLength || str.length;\n
      if (heredoc && str.length > 0 && str[0] === \'\\n\') {\n
        str = str.slice(1);\n
        strOffset++;\n
      }\n
      tokens = [];\n
      pi = 0;\n
      i = -1;\n
      while (letter = str.charAt(i += 1)) {\n
        if (letter === \'\\\\\') {\n
          i += 1;\n
          continue;\n
        }\n
        if (!(letter === \'#\' && str.charAt(i + 1) === \'{\' && (expr = this.balancedString(str.slice(i + 1), \'}\')))) {\n
          continue;\n
        }\n
        if (pi < i) {\n
          tokens.push(this.makeToken(\'NEOSTRING\', str.slice(pi, i), strOffset + pi));\n
        }\n
        inner = expr.slice(1, -1);\n
        if (inner.length) {\n
          _ref2 = this.getLineAndColumnFromChunk(strOffset + i + 1), line = _ref2[0], column = _ref2[1];\n
          nested = new Lexer().tokenize(inner, {\n
            line: line,\n
            column: column,\n
            rewrite: false\n
          });\n
          popped = nested.pop();\n
          if (((_ref3 = nested[0]) != null ? _ref3[0] : void 0) === \'TERMINATOR\') {\n
            popped = nested.shift();\n
          }\n
          if (len = nested.length) {\n
            if (len > 1) {\n
              nested.unshift(this.makeToken(\'(\', \'(\', strOffset + i + 1, 0));\n
              nested.push(this.makeToken(\')\', \')\', strOffset + i + 1 + inner.length, 0));\n
            }\n
            tokens.push([\'TOKENS\', nested]);\n
          }\n
        }\n
        i += expr.length;\n
        pi = i + 1;\n
      }\n
      if ((i > pi && pi < str.length)) {\n
        tokens.push(this.makeToken(\'NEOSTRING\', str.slice(pi), strOffset + pi));\n
      }\n
      if (regex) {\n
        return tokens;\n
      }\n
      if (!tokens.length) {\n
        return this.token(\'STRING\', \'""\', offsetInChunk, lexedLength);\n
      }\n
      if (tokens[0][0] !== \'NEOSTRING\') {\n
        tokens.unshift(this.makeToken(\'NEOSTRING\', \'\', offsetInChunk));\n
      }\n
      if (interpolated = tokens.length > 1) {\n
        this.token(\'(\', \'(\', offsetInChunk, 0);\n
      }\n
      for (i = _i = 0, _len = tokens.length; _i < _len; i = ++_i) {\n
        token = tokens[i];\n
        tag = token[0], value = token[1];\n
        if (i) {\n
          if (i) {\n
            plusToken = this.token(\'+\', \'+\');\n
          }\n
          locationToken = tag === \'TOKENS\' ? value[0] : token;\n
          plusToken[2] = {\n
            first_line: locationToken[2].first_line,\n
            first_column: locationToken[2].first_column,\n
            last_line: locationToken[2].first_line,\n
            last_column: locationToken[2].first_column\n
          };\n
        }\n
        if (tag === \'TOKENS\') {\n
          (_ref4 = this.tokens).push.apply(_ref4, value);\n
        } else if (tag === \'NEOSTRING\') {\n
          token[0] = \'STRING\';\n
          token[1] = this.makeString(value, \'"\', heredoc);\n
          this.tokens.push(token);\n
        } else {\n
          this.error("Unexpected " + tag);\n
        }\n
      }\n
      if (interpolated) {\n
        rparen = this.makeToken(\')\', \')\', offsetInChunk + lexedLength, 0);\n
        rparen.stringEnd = true;\n
        this.tokens.push(rparen);\n
      }\n
      return tokens;\n
    };\n
\n
    Lexer.prototype.pair = function(tag) {\n
      var size, wanted;\n
      if (tag !== (wanted = last(this.ends))) {\n
        if (\'OUTDENT\' !== wanted) {\n
          this.error("unmatched " + tag);\n
        }\n
        this.indent -= size = last(this.indents);\n
        this.outdentToken(size, true);\n
        return this.pair(tag);\n
      }\n
      return this.ends.pop();\n
    };\n
\n
    Lexer.prototype.getLineAndColumnFromChunk = function(offset) {\n
      var column, lineCount, lines, string;\n
      if (offset === 0) {\n
        return [this.chunkLine, this.chunkColumn];\n
      }\n
      if (offset >= this.chunk.length) {\n
        string = this.chunk;\n
      } else {\n
        string = this.chunk.slice(0, +(offset - 1) + 1 || 9e9);\n
      }\n
      lineCount = count(string, \'\\n\');\n
      column = this.chunkColumn;\n
      if (lineCount > 0) {\n
        lines = string.split(\'\\n\');\n
        column = last(lines).length;\n
      } else {\n
        column += string.length;\n
      }\n
      return [this.chunkLine + lineCount, column];\n
    };\n
\n
    Lexer.prototype.makeToken = function(tag, value, offsetInChunk, length) {\n
      var lastCharacter, locationData, token, _ref2, _ref3;\n
      if (offsetInChunk == null) {\n
        offsetInChunk = 0;\n
      }\n
      if (length == null) {\n
        length = value.length;\n
      }\n
      locationData = {};\n
      _ref2 = this.getLineAndColumnFromChunk(offsetInChunk), locationData.first_line = _ref2[0], locationData.first_column = _ref2[1];\n
      lastCharacter = Math.max(0, length - 1);\n
      _ref3 = this.getLineAndColumnFromChunk(offsetInChunk + lastCharacter), locationData.last_line = _ref3[0], locationData.last_column = _ref3[1];\n
      token = [tag, value, locationData];\n
      return token;\n
    };\n
\n
    Lexer.prototype.token = function(tag, value, offsetInChunk, length) {\n
      var token;\n
      token = this.makeToken(tag, value, offsetInChunk, length);\n
      this.tokens.push(token);\n
      return token;\n
    };\n
\n
    Lexer.prototype.tag = function(index, tag) {\n
      var tok;\n
      return (tok = last(this.tokens, index)) && (tag ? tok[0] = tag : tok[0]);\n
    };\n
\n
    Lexer.prototype.value = function(index, val) {\n
      var tok;\n
      return (tok = last(this.tokens, index)) && (val ? tok[1] = val : tok[1]);\n
    };\n
\n
    Lexer.prototype.unfinished = function() {\n
      var _ref2;\n
      return LINE_CONTINUER.test(this.chunk) || ((_ref2 = this.tag()) === \'\\\\\' || _ref2 === \'.\' || _ref2 === \'?.\' || _ref2 === \'?::\' || _ref2 === \'UNARY\' || _ref2 === \'MATH\' || _ref2 === \'+\' || _ref2 === \'-\' || _ref2 === \'SHIFT\' || _ref2 === \'RELATION\' || _ref2 === \'COMPARE\' || _ref2 === \'LOGIC\' || _ref2 === \'THROW\' || _ref2 === \'EXTENDS\');\n
    };\n
\n
    Lexer.prototype.escapeLines = function(str, heredoc) {\n
      return str.replace(MULTILINER, heredoc ? \'\\\\n\' : \'\');\n
    };\n
\n
    Lexer.prototype.makeString = function(body, quote, heredoc) {\n
      if (!body) {\n
        return quote + quote;\n
      }\n
      body = body.replace(/\\\\([\\s\\S])/g, function(match, contents) {\n
        if (contents === \'\\n\' || contents === quote) {\n
          return contents;\n
        } else {\n
          return match;\n
        }\n
      });\n
      body = body.replace(RegExp("" + quote, "g"), \'\\\\$&\');\n
      return quote + this.escapeLines(body, heredoc) + quote;\n
    };\n
\n
    Lexer.prototype.error = function(message, offset) {\n
      var first_column, first_line, _ref2;\n
      if (offset == null) {\n
        offset = 0;\n
      }\n
      _ref2 = this.getLineAndColumnFromChunk(offset), first_line = _ref2[0], first_column = _ref2[1];\n
      return throwSyntaxError(message, {\n
        first_line: first_line,\n
        first_column: first_column\n
      });\n
    };\n
\n
    return Lexer;\n
\n
  })();\n
\n
  JS_KEYWORDS = [\'true\', \'false\', \'null\', \'this\', \'new\', \'delete\', \'typeof\', \'in\', \'instanceof\', \'return\', \'throw\', \'break\', \'continue\', \'debugger\', \'if\', \'else\', \'switch\', \'for\', \'while\', \'do\', \'try\', \'catch\', \'finally\', \'class\', \'extends\', \'super\'];\n
\n
  COFFEE_KEYWORDS = [\'undefined\', \'then\', \'unless\', \'until\', \'loop\', \'of\', \'by\', \'when\'];\n
\n
  COFFEE_ALIAS_MAP = {\n
    and: \'&&\',\n
    or: \'||\',\n
    is: \'==\',\n
    isnt: \'!=\',\n
    not: \'!\',\n
    yes: \'true\',\n
    no: \'false\',\n
    on: \'true\',\n
    off: \'false\'\n
  };\n
\n
  COFFEE_ALIASES = (function() {\n
    var _results;\n
    _results = [];\n
    for (key in COFFEE_ALIAS_MAP) {\n
      _results.push(key);\n
    }\n
    return _results;\n
  })();\n
\n
  COFFEE_KEYWORDS = COFFEE_KEYWORDS.concat(COFFEE_ALIASES);\n
\n
  RESERVED = [\'case\', \'default\', \'function\', \'var\', \'void\', \'with\', \'const\', \'let\', \'enum\', \'export\', \'import\', \'native\', \'__hasProp\', \'__extends\', \'__slice\', \'__bind\', \'__indexOf\', \'implements\', \'interface\', \'package\', \'private\', \'protected\', \'public\', \'static\', \'yield\'];\n
\n
  STRICT_PROSCRIBED = [\'arguments\', \'eval\'];\n
\n
  JS_FORBIDDEN = JS_KEYWORDS.concat(RESERVED).concat(STRICT_PROSCRIBED);\n
\n
  exports.RESERVED = RESERVED.concat(JS_KEYWORDS).concat(COFFEE_KEYWORDS).concat(STRICT_PROSCRIBED);\n
\n
  exports.STRICT_PROSCRIBED = STRICT_PROSCRIBED;\n
\n
  BOM = 65279;\n
\n
  IDENTIFIER = /^([$A-Za-z_\\x7f-\\uffff][$\\w\\x7f-\\uffff]*)([^\\n\\S]*:(?!:))?/;\n
\n
  NUMBER = /^0b[01]+|^0o[0-7]+|^0x[\\da-f]+|^\\d*\\.?\\d+(?:e[+-]?\\d+)?/i;\n
\n
  HEREDOC = /^("""|\'\'\')([\\s\\S]*?)(?:\\n[^\\n\\S]*)?\\1/;\n
\n
  OPERATOR = /^(?:[-=]>|[-+*\\/%<>&|^!?=]=|>>>=?|([-+:])\\1|([&|<>])\\2=?|\\?(\\.|::)|\\.{2,3})/;\n
\n
  WHITESPACE = /^[^\\n\\S]+/;\n
\n
  COMMENT = /^###([^#][\\s\\S]*?)(?:###[^\\n\\S]*|(?:###)$)|^(?:\\s*#(?!##[^#]).*)+/;\n
\n
  CODE = /^[-=]>/;\n
\n
  MULTI_DENT = /^(?:\\n[^\\n\\S]*)+/;\n
\n
  SIMPLESTR = /^\'[^\\\\\']*(?:\\\\.[^\\\\\']*)*\'/;\n
\n
  JSTOKEN = /^`[^\\\\`]*(?:\\\\.[^\\\\`]*)*`/;\n
\n
  REGEX = /^(\\/(?![\\s=])[^[\\/\\n\\\\]*(?:(?:\\\\[\\s\\S]|\\[[^\\]\\n\\\\]*(?:\\\\[\\s\\S][^\\]\\n\\\\]*)*])[^[\\/\\n\\\\]*)*\\/)([imgy]{0,4})(?!\\w)/;\n
\n
  HEREGEX = /^\\/{3}([\\s\\S]+?)\\/{3}([imgy]{0,4})(?!\\w)/;\n
\n
  HEREGEX_OMIT = /\\s+(?:#.*)?/g;\n
\n
  MULTILINER = /\\n/g;\n
\n
  HEREDOC_INDENT = /\\n+([^\\n\\S]*)/g;\n
\n
  HEREDOC_ILLEGAL = /\\*\\//;\n
\n
  LINE_CONTINUER = /^\\s*(?:,|\\??\\.(?![.\\d])|::)/;\n
\n
  TRAILING_SPACES = /\\s+$/;\n
\n
  COMPOUND_ASSIGN = [\'-=\', \'+=\', \'/=\', \'*=\', \'%=\', \'||=\', \'&&=\', \'?=\', \'<<=\', \'>>=\', \'>>>=\', \'&=\', \'^=\', \'|=\'];\n
\n
  UNARY = [\'!\', \'~\', \'NEW\', \'TYPEOF\', \'DELETE\', \'DO\'];\n
\n
  LOGIC = [\'&&\', \'||\', \'&\', \'|\', \'^\'];\n
\n
  SHIFT = [\'<<\', \'>>\', \'>>>\'];\n
\n
  COMPARE = [\'==\', \'!=\', \'<\', \'>\', \'<=\', \'>=\'];\n
\n
  MATH = [\'*\', \'/\', \'%\'];\n
\n
  RELATION = [\'IN\', \'OF\', \'INSTANCEOF\'];\n
\n
  BOOL = [\'TRUE\', \'FALSE\'];\n
\n
  NOT_REGEX = [\'NUMBER\', \'REGEX\', \'BOOL\', \'NULL\', \'UNDEFINED\', \'++\', \'--\'];\n
\n
  NOT_SPACED_REGEX = NOT_REGEX.concat(\')\', \'}\', \'THIS\', \'IDENTIFIER\', \'STRING\', \']\');\n
\n
  CALLABLE = [\'IDENTIFIER\', \'STRING\', \'REGEX\', \')\', \']\', \'}\', \'?\', \'::\', \'@\', \'THIS\', \'SUPER\'];\n
\n
  INDEXABLE = CALLABLE.concat(\'NUMBER\', \'BOOL\', \'NULL\', \'UNDEFINED\');\n
\n
  LINE_BREAK = [\'INDENT\', \'OUTDENT\', \'TERMINATOR\'];\n
\n
\n
});\n
\n
define(\'ace/mode/coffee/rewriter\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
  var BALANCED_PAIRS, EXPRESSION_CLOSE, EXPRESSION_END, EXPRESSION_START, IMPLICIT_CALL, IMPLICIT_END, IMPLICIT_FUNC, IMPLICIT_UNSPACED_CALL, INVERSES, LINEBREAKS, SINGLE_CLOSERS, SINGLE_LINERS, generate, left, rite, _i, _len, _ref,\n
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; },\n
    __slice = [].slice;\n
\n
  generate = function(tag, value) {\n
    var tok;\n
    tok = [tag, value];\n
    tok.generated = true;\n
    return tok;\n
  };\n
\n
  exports.Rewriter = (function() {\n
    function Rewriter() {}\n
\n
    Rewriter.prototype.rewrite = function(tokens) {\n
      this.tokens = tokens;\n
      this.removeLeadingNewlines();\n
      this.removeMidExpressionNewlines();\n
      this.closeOpenCalls();\n
      this.closeOpenIndexes();\n
      this.addImplicitIndentation();\n
      this.tagPostfixConditionals();\n
      this.addImplicitBracesAndParens();\n
      this.addLocationDataToGeneratedTokens();\n
      return this.tokens;\n
    };\n
\n
    Rewriter.prototype.scanTokens = function(block) {\n
      var i, token, tokens;\n
      tokens = this.tokens;\n
      i = 0;\n
      while (token = tokens[i]) {\n
        i += block.call(this, token, i, tokens);\n
      }\n
      return true;\n
    };\n
\n
    Rewriter.prototype.detectEnd = function(i, condition, action) {\n
      var levels, token, tokens, _ref, _ref1;\n
      tokens = this.tokens;\n
      levels = 0;\n
      while (token = tokens[i]) {\n
        if (levels === 0 && condition.call(this, token, i)) {\n
          return action.call(this, token, i);\n
        }\n
        if (!token || levels < 0) {\n
          return action.call(this, token, i - 1);\n
        }\n
        if (_ref = token[0], __indexOf.call(EXPRESSION_START, _ref) >= 0) {\n
          levels += 1;\n
        } else if (_ref1 = token[0], __indexOf.call(EXPRESSION_END, _ref1) >= 0) {\n
          levels -= 1;\n
        }\n
        i += 1;\n
      }\n
      return i - 1;\n
    };\n
\n
    Rewriter.prototype.removeLeadingNewlines = function() {\n
      var i, tag, _i, _len, _ref;\n
      _ref = this.tokens;\n
      for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {\n
        tag = _ref[i][0];\n
        if (tag !== \'TERMINATOR\') {\n
          break;\n
        }\n
      }\n
      if (i) {\n
        return this.tokens.splice(0, i);\n
      }\n
    };\n
\n
    Rewriter.prototype.removeMidExpressionNewlines = function() {\n
      return this.scanTokens(function(token, i, tokens) {\n
        var _ref;\n
        if (!(token[0] === \'TERMINATOR\' && (_ref = this.tag(i + 1), __indexOf.call(EXPRESSION_CLOSE, _ref) >= 0))) {\n
          return 1;\n
        }\n
        tokens.splice(i, 1);\n
        return 0;\n
      });\n
    };\n
\n
    Rewriter.prototype.closeOpenCalls = function() {\n
      var action, condition;\n
      condition = function(token, i) {\n
        var _ref;\n
        return ((_ref = token[0]) === \')\' || _ref === \'CALL_END\') || token[0] === \'OUTDENT\' && this.tag(i - 1) === \')\';\n
      };\n
      action = function(token, i) {\n
        return this.tokens[token[0] === \'OUTDENT\' ? i - 1 : i][0] = \'CALL_END\';\n
      };\n
      return this.scanTokens(function(token, i) {\n
        if (token[0] === \'CALL_START\') {\n
          this.detectEnd(i + 1, condition, action);\n
        }\n
        return 1;\n
      });\n
    };\n
\n
    Rewriter.prototype.closeOpenIndexes = function() {\n
      var action, condition;\n
      condition = function(token, i) {\n
        var _ref;\n
        return (_ref = token[0]) === \']\' || _ref === \'INDEX_END\';\n
      };\n
      action = function(token, i) {\n
        return token[0] = \'INDEX_END\';\n
      };\n
      return this.scanTokens(function(token, i) {\n
        if (token[0] === \'INDEX_START\') {\n
          this.detectEnd(i + 1, condition, action);\n
        }\n
        return 1;\n
      });\n
    };\n
\n
    Rewriter.prototype.matchTags = function() {\n
      var fuzz, i, j, pattern, _i, _ref, _ref1;\n
      i = arguments[0], pattern = 2 <= arguments.length ? __slice.call(arguments, 1) : [];\n
      fuzz = 0;\n
      for (j = _i = 0, _ref = pattern.length; 0 <= _ref ? _i < _ref : _i > _ref; j = 0 <= _ref ? ++_i : --_i) {\n
        while (this.tag(i + j + fuzz) === \'HERECOMMENT\') {\n
          fuzz += 2;\n
        }\n
        if (pattern[j] == null) {\n
          continue;\n
        }\n
        if (typeof pattern[j] === \'string\') {\n
          pattern[j] = [pattern[j]];\n
        }\n
        if (_ref1 = this.tag(i + j + fuzz), __indexOf.call(pattern[j], _ref1) < 0) {\n
          return false;\n
        }\n
      }\n
      return true;\n
    };\n
\n
    Rewriter.prototype.looksObjectish = function(j) {\n
      return this.matchTags(j, \'@\', null, \':\') || this.matchTags(j, null, \':\');\n
    };\n
\n
    Rewriter.prototype.findTagsBackwards = function(i, tags) {\n
      var backStack, _ref, _ref1, _ref2, _ref3, _ref4, _ref5;\n
      backStack = [];\n
      while (i >= 0 && (backStack.length || (_ref2 = this.tag(i), __indexOf.call(tags, _ref2) < 0) && ((_ref3 = this.tag(i), __indexOf.call(EXPRESSION_START, _ref3) < 0) || this.tokens[i].generated) && (_ref4 = this.tag(i), __indexOf.call(LINEBREAKS, _ref4) < 0))) {\n
        if (_ref = this.tag(i), __indexOf.call(EXPRESSION_END, _ref) >= 0) {\n
          backStack.push(this.tag(i));\n
        }\n
        if ((_ref1 = this.tag(i), __indexOf.call(EXPRESSION_START, _ref1) >= 0) && backStack.length) {\n
          backStack.pop();\n
        }\n
        i -= 1;\n
      }\n
      return _ref5 = this.tag(i), __indexOf.call(tags, _ref5) >= 0;\n
    };\n
\n
    Rewriter.prototype.addImplicitBracesAndParens = function() {\n
      var stack;\n
      stack = [];\n
      return this.scanTokens(function(token, i, tokens) {\n
        var endImplicitCall, endImplicitObject, forward, inImplicit, inImplicitCall, inImplicitControl, inImplicitObject, nextTag, offset, prevTag, s, sameLine, stackIdx, stackTag, stackTop, startIdx, startImplicitCall, startImplicitObject, startsLine, tag, _ref, _ref1, _ref2, _ref3, _ref4, _ref5;\n
        tag = token[0];\n
        prevTag = (i > 0 ? tokens[i - 1] : [])[0];\n
        nextTag = (i < tokens.length - 1 ? tokens[i + 1] : [])[0];\n
        stackTop = function() {\n
          return stack[stack.length - 1];\n
        };\n
        startIdx = i;\n
        forward = function(n) {\n
          return i - startIdx + n;\n
        };\n
        inImplicit = function() {\n
          var _ref, _ref1;\n
          return (_ref = stackTop()) != null ? (_ref1 = _ref[2]) != null ? _ref1.ours : void 0 : void 0;\n
        };\n
        inImplicitCall = function() {\n
          var _ref;\n
          return inImplicit() && ((_ref = stackTop()) != null ? _ref[0] : void 0) === \'(\';\n
        };\n
        inImplicitObject = function() {\n
          var _ref;\n
          return inImplicit() && ((_ref = stackTop()) != null ? _ref[0] : void 0) === \'{\';\n
        };\n
        inImplicitControl = function() {\n
          var _ref;\n
          return inImplicit && ((_ref = stackTop()) != null ? _ref[0] : void 0) === \'CONTROL\';\n
        };\n
        startImplicitCall = function(j) {\n
          var idx;\n
          idx = j != null ? j : i;\n
          stack.push([\n
            \'(\', idx, {\n
              ours: true\n
            }\n
          ]);\n
          tokens.splice(idx, 0, generate(\'CALL_START\', \'(\'));\n
          if (j == null) {\n
            return i += 1;\n
          }\n
        };\n
        endImplicitCall = function() {\n
          stack.pop();\n
          tokens.splice(i, 0, generate(\'CALL_END\', \')\'));\n
          return i += 1;\n
        };\n
        startImplicitObject = function(j, startsLine) {\n
          var idx;\n
          if (startsLine == null) {\n
            startsLine = true;\n
          }\n
          idx = j != null ? j : i;\n
          stack.push([\n
            \'{\', idx, {\n
              sameLine: true,\n
              startsLine: startsLine,\n
              ours: true\n
            }\n
          ]);\n
          tokens.splice(idx, 0, generate(\'{\', generate(new String(\'{\'))));\n
          if (j == null) {\n
            return i += 1;\n
          }\n
        };\n
        endImplicitObject = function(j) {\n
          j = j != null ? j : i;\n
          stack.pop();\n
          tokens.splice(j, 0, generate(\'}\', \'}\'));\n
          return i += 1;\n
        };\n
        if (inImplicitCall() && (tag === \'IF\' || tag === \'TRY\' || tag === \'FINALLY\' || tag === \'CATCH\' || tag === \'CLASS\' || tag === \'SWITCH\')) {\n
          stack.push([\n
            \'CONTROL\', i, {\n
              ours: true\n
            }\n
          ]);\n
          return forward(1);\n
        }\n
        if (tag === \'INDENT\' && inImplicit()) {\n
          if (prevTag !== \'=>\' && prevTag !== \'->\' && prevTag !== \'[\' && prevTag !== \'(\' && prevTag !== \',\' && prevTag !== \'{\' && prevTag !== \'TRY\' && prevTag !== \'ELSE\' && prevTag !== \'=\') {\n
            while (inImplicitCall()) {\n
              endImplicitCall();\n
            }\n
          }\n
          if (inImplicitControl()) {\n
            stack.pop();\n
          }\n
          stack.push([tag, i]);\n
          return forward(1);\n
        }\n
        if (__indexOf.call(EXPRESSION_START, tag) >= 0) {\n
          stack.push([tag, i]);\n
          return forward(1);\n
        }\n
        if (__indexOf.call(EXPRESSION_END, tag) >= 0) {\n
          while (inImplicit()) {\n
            if (inImplicitCall()) {\n
              endImplicitCall();\n
            } else if (inImplicitObject()) {\n
              endImplicitObject();\n
            } else {\n
              stack.pop();\n
            }\n
          }\n
          stack.pop();\n
        }\n
        if ((__indexOf.call(IMPLICIT_FUNC, tag) >= 0 && token.spaced && !token.stringEnd || tag === \'?\' && i > 0 && !tokens[i - 1].spaced) && (__indexOf.call(IMPLICIT_CALL, nextTag) >= 0 || __indexOf.call(IMPLICIT_UNSPACED_CALL, nextTag) >= 0 && !((_ref = tokens[i + 1]) != null ? _ref.spaced : void 0) && !((_ref1 = tokens[i + 1]) != null ? _ref1.newLine : void 0))) {\n
          if (tag === \'?\') {\n
            tag = token[0] = \'FUNC_EXIST\';\n
          }\n
          startImplicitCall(i + 1);\n
          return forward(2);\n
        }\n
        if (__indexOf.call(IMPLICIT_FUNC, tag) >= 0 && this.matchTags(i + 1, \'INDENT\', null, \':\') && !this.findTagsBackwards(i, [\'CLASS\', \'EXTENDS\', \'IF\', \'CATCH\', \'SWITCH\', \'LEADING_WHEN\', \'FOR\', \'WHILE\', \'UNTIL\'])) {\n
          startImplicitCall(i + 1);\n
          stack.push([\'INDENT\', i + 2]);\n
          return forward(3);\n
        }\n
        if (tag === \':\') {\n
          if (this.tag(i - 2) === \'@\') {\n
            s = i - 2;\n
          } else {\n
            s = i - 1;\n
          }\n
          while (this.tag(s - 2) === \'HERECOMMENT\') {\n
            s -= 2;\n
          }\n
          startsLine = s === 0 || (_ref2 = this.tag(s - 1), __indexOf.call(LINEBREAKS, _ref2) >= 0) || tokens[s - 1].newLine;\n
          if (stackTop()) {\n
            _ref3 = stackTop(), stackTag = _ref3[0], stackIdx = _ref3[1];\n
            if ((stackTag === \'{\' || stackTag === \'INDENT\' && this.tag(stackIdx - 1) === \'{\') && (startsLine || this.tag(s - 1) === \',\' || this.tag(s - 1) === \'{\')) {\n
              return forward(1);\n
            }\n
          }\n
          startImplicitObject(s, !!startsLine);\n
          return forward(2);\n
        }\n
        if (prevTag === \'OUTDENT\' && inImplicitCall() && (tag === \'.\' || tag === \'?.\' || tag === \'::\' || tag === \'?::\')) {\n
          endImplicitCall();\n
          return forward(1);\n
        }\n
        if (inImplicitObject() && __indexOf.call(LINEBREAKS, tag) >= 0) {\n
          stackTop()[2].sameLine = false;\n
        }\n
        if (__indexOf.call(IMPLICIT_END, tag) >= 0) {\n
          while (inImplicit()) {\n
            _ref4 = stackTop(), stackTag = _ref4[0], stackIdx = _ref4[1], (_ref5 = _ref4[2], sameLine = _ref5.sameLine, startsLine = _ref5.startsLine);\n
            if (inImplicitCall() && prevTag !== \',\') {\n
              endImplicitCall();\n
            } else if (inImplicitObject() && sameLine && !startsLine) {\n
              endImplicitObject();\n
            } else if (inImplicitObject() && tag === \'TERMINATOR\' && prevTag !== \',\' && !(startsLine && this.looksObjectish(i + 1))) {\n
              endImplicitObject();\n
            } else {\n
              break;\n
            }\n
          }\n
        }\n
        if (tag === \',\' && !this.looksObjectish(i + 1) && inImplicitObject() && (nextTag !== \'TERMINATOR\' || !this.looksObjectish(i + 2))) {\n
          offset = nextTag === \'OUTDENT\' ? 1 : 0;\n
          while (inImplicitObject()) {\n
            endImplicitObject(i + offset);\n
          }\n
        }\n
        return forward(1);\n
      });\n
    };\n
\n
    Rewriter.prototype.addLocationDataToGeneratedTokens = function() {\n
      return this.scanTokens(function(token, i, tokens) {\n
        var column, line, nextLocation, prevLocation, _ref, _ref1;\n
        if (token[2]) {\n
          return 1;\n
        }\n
        if (!(token.generated || token.explicit)) {\n
          return 1;\n
        }\n
        if (token[0] === \'{\' && (nextLocation = (_ref = tokens[i + 1]) != null ? _ref[2] : void 0)) {\n
          line = nextLocation.first_line, column = nextLocation.first_column;\n
        } else if (prevLocation = (_ref1 = tokens[i - 1]) != null ? _ref1[2] : void 0) {\n
          line = prevLocation.last_line, column = prevLocation.last_column;\n
        } else {\n
          line = column = 0;\n
        }\n
        token[2] = {\n
          first_line: line,\n
          first_column: column,\n
          last_line: line,\n
          last_column: column\n
        };\n
        return 1;\n
      });\n
    };\n
\n
    Rewriter.prototype.addImplicitIndentation = function() {\n
      var action, condition, indent, outdent, starter;\n
      starter = indent = outdent = null;\n
      condition = function(token, i) {\n
        var _ref, _ref1;\n
        return token[1] !== \';\' && (_ref = token[0], __indexOf.call(SINGLE_CLOSERS, _ref) >= 0) && !(token[0] === \'ELSE\' && starter !== \'THEN\') && !(((_ref1 = token[0]) === \'CATCH\' || _ref1 === \'FINALLY\') && (starter === \'->\' || starter === \'=>\'));\n
      };\n
      action = function(token, i) {\n
        return this.tokens.splice((this.tag(i - 1) === \',\' ? i - 1 : i), 0, outdent);\n
      };\n
      return this.scanTokens(function(token, i, tokens) {\n
        var j, tag, _i, _ref, _ref1;\n
        tag = token[0];\n
        if (tag === \'TERMINATOR\' && this.tag(i + 1) === \'THEN\') {\n
          tokens.splice(i, 1);\n
          return 0;\n
        }\n
        if (tag === \'ELSE\' && this.tag(i - 1) !== \'OUTDENT\') {\n
          tokens.splice.apply(tokens, [i, 0].concat(__slice.call(this.indentation())));\n
          return 2;\n
        }\n
        if (tag === \'CATCH\') {\n
          for (j = _i = 1; _i <= 2; j = ++_i) {\n
            if (!((_ref = this.tag(i + j)) === \'OUTDENT\' || _ref === \'TERMINATOR\' || _ref === \'FINALLY\')) {\n
              continue;\n
            }\n
            tokens.splice.apply(tokens, [i + j, 0].concat(__slice.call(this.indentation())));\n
            return 2 + j;\n
          }\n
        }\n
        if (__indexOf.call(SINGLE_LINERS, tag) >= 0 && this.tag(i + 1) !== \'INDENT\' && !(tag === \'ELSE\' && this.tag(i + 1) === \'IF\')) {\n
          starter = tag;\n
          _ref1 = this.indentation(true), indent = _ref1[0], outdent = _ref1[1];\n
          if (starter === \'THEN\') {\n
            indent.fromThen = true;\n
          }\n
          tokens.splice(i + 1, 0, indent);\n
          this.detectEnd(i + 2, condition, action);\n
          if (tag === \'THEN\') {\n
            tokens.splice(i, 1);\n
          }\n
          return 1;\n
        }\n
        return 1;\n
      });\n
    };\n
\n
    Rewriter.prototype.tagPostfixConditionals = function() {\n
      var action, condition, original;\n
      original = null;\n
      condition = function(token, i) {\n
        var prevTag, tag;\n
        tag = token[0];\n
        prevTag = this.tokens[i - 1][0];\n
        return tag === \'TERMINATOR\' || (tag === \'INDENT\' && __indexOf.call(SINGLE_LINERS, prevTag) < 0);\n
      };\n
      action = function(token, i) {\n
        if (token[0] !== \'INDENT\' || (token.generated && !token.fromThen)) {\n
          return original[0] = \'POST_\' + original[0];\n
        }\n
      };\n
      return this.scanTokens(function(token, i) {\n
        if (token[0] !== \'IF\') {\n
          return 1;\n
        }\n
        original = token;\n
        this.detectEnd(i + 1, condition, action);\n
        return 1;\n
      });\n
    };\n
\n
    Rewriter.prototype.indentation = function(implicit) {\n
      var indent, outdent;\n
      if (implicit == null) {\n
        implicit = false;\n
      }\n
      indent = [\'INDENT\', 2];\n
      outdent = [\'OUTDENT\', 2];\n
      if (implicit) {\n
        indent.generated = outdent.generated = true;\n
      }\n
      if (!implicit) {\n
        indent.explicit = outdent.explicit = true;\n
      }\n
      return [indent, outdent];\n
    };\n
\n
    Rewriter.prototype.generate = generate;\n
\n
    Rewriter.prototype.tag = function(i) {\n
      var _ref;\n
      return (_ref = this.tokens[i]) != null ? _ref[0] : void 0;\n
    };\n
\n
    return Rewriter;\n
\n
  })();\n
\n
  BALANCED_PAIRS = [[\'(\', \')\'], [\'[\', \']\'], [\'{\', \'}\'], [\'INDENT\', \'OUTDENT\'], [\'CALL_START\', \'CALL_END\'], [\'PARAM_START\', \'PARAM_END\'], [\'INDEX_START\', \'INDEX_END\']];\n
\n
  exports.INVERSES = INVERSES = {};\n
\n
  EXPRESSION_START = [];\n
\n
  EXPRESSION_END = [];\n
\n
  for (_i = 0, _len = BALANCED_PAIRS.length; _i < _len; _i++) {\n
    _ref = BALANCED_PAIRS[_i], left = _ref[0], rite = _ref[1];\n
    EXPRESSION_START.push(INVERSES[rite] = left);\n
    EXPRESSION_END.push(INVERSES[left] = rite);\n
  }\n
\n
  EXPRESSION_CLOSE = [\'CATCH\', \'WHEN\', \'ELSE\', \'FINALLY\'].concat(EXPRESSION_END);\n
\n
  IMPLICIT_FUNC = [\'IDENTIFIER\', \'SUPER\', \')\', \'CALL_END\', \']\', \'INDEX_END\', \'@\', \'THIS\'];\n
\n
  IMPLICIT_CALL = [\'IDENTIFIER\', \'NUMBER\', \'STRING\', \'JS\', \'REGEX\', \'NEW\', \'PARAM_START\', \'CLASS\', \'IF\', \'TRY\', \'SWITCH\', \'THIS\', \'BOOL\', \'NULL\', \'UNDEFINED\', \'UNARY\', \'SUPER\', \'THROW\', \'@\', \'->\', \'=>\', \'[\', \'(\', \'{\', \'--\', \'++\'];\n
\n
  IMPLICIT_UNSPACED_CALL = [\'+\', \'-\'];\n
\n
  IMPLICIT_END = [\'POST_IF\', \'FOR\', \'WHILE\', \'UNTIL\', \'WHEN\', \'BY\', \'LOOP\', \'TERMINATOR\'];\n
\n
  SINGLE_LINERS = [\'ELSE\', \'->\', \'=>\', \'TRY\', \'FINALLY\', \'THEN\'];\n
\n
  SINGLE_CLOSERS = [\'TERMINATOR\', \'CATCH\', \'FINALLY\', \'ELSE\', \'OUTDENT\', \'LEADING_WHEN\'];\n
\n
  LINEBREAKS = [\'TERMINATOR\', \'INDENT\', \'OUTDENT\'];\n
\n
\n
});\n
\n
define(\'ace/mode/coffee/helpers\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
  var buildLocationData, extend, flatten, last, repeat, syntaxErrorToString, _ref;\n
\n
  exports.starts = function(string, literal, start) {\n
    return literal === string.substr(start, literal.length);\n
  };\n
\n
  exports.ends = function(string, literal, back) {\n
    var len;\n
    len = literal.length;\n
    return literal === string.substr(string.length - len - (back || 0), len);\n
  };\n
\n
  exports.repeat = repeat = function(str, n) {\n
    var res;\n
    res = \'\';\n
    while (n > 0) {\n
      if (n & 1) {\n
        res += str;\n
      }\n
      n >>>= 1;\n
      str += str;\n
    }\n
    return res;\n
  };\n
\n
  exports.compact = function(array) {\n
    var item, _i, _len, _results;\n
    _results = [];\n
    for (_i = 0, _len = array.length; _i < _len; _i++) {\n
      item = array[_i];\n
      if (item) {\n
        _results.push(item);\n
      }\n
    }\n
    return _results;\n
  };\n
\n
  exports.count = function(string, substr) {\n
    var num, pos;\n
    num = pos = 0;\n
    if (!substr.length) {\n
      return 1 / 0;\n
    }\n
    while (pos = 1 + string.indexOf(substr, pos)) {\n
      num++;\n
    }\n
    return num;\n
  };\n
\n
  exports.merge = function(options, overrides) {\n
    return extend(extend({}, options), overrides);\n
  };\n
\n
  extend = exports.extend = function(object, properties) {\n
    var key, val;\n
    for (key in properties) {\n
      val = properties[key];\n
      object[key] = val;\n
    }\n
    return object;\n
  };\n
\n
  exports.flatten = flatten = function(array) {\n
    var element, flattened, _i, _len;\n
    flattened = [];\n
    for (_i = 0, _len = array.length; _i < _len; _i++) {\n
      element = array[_i];\n
      if (element instanceof Array) {\n
        flattened = flattened.concat(flatten(element));\n
      } else {\n
        flattened.push(element);\n
      }\n
    }\n
    return flattened;\n
  };\n
\n
  exports.del = function(obj, key) {\n
    var val;\n
    val = obj[key];\n
    delete obj[key];\n
    return val;\n
  };\n
\n
  exports.last = last = function(array, back) {\n
    return array[array.length - (back || 0) - 1];\n
  };\n
\n
  exports.some = (_ref = Array.prototype.some) != null ? _ref : function(fn) {\n
    var e, _i, _len;\n
    for (_i = 0, _len = this.length; _i < _len; _i++) {\n
      e = this[_i];\n
      if (fn(e)) {\n
        return true;\n
      }\n
    }\n
    return false;\n
  };\n
\n
  exports.invertLiterate = function(code) {\n
    var line, lines, maybe_code;\n
    maybe_code = true;\n
    lines = (function() {\n
      var _i, _len, _ref1, _results;\n
      _ref1 = code.split(\'\\n\');\n
      _results = [];\n
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {\n
        line = _ref1[_i];\n
        if (maybe_code && /^([ ]{4}|[ ]{0,3}\\t)/.test(line)) {\n
          _results.push(line);\n
        } else if (maybe_code = /^\\s*$/.test(line)) {\n
          _results.push(line);\n
        } else {\n
          _results.push(\'# \' + line);\n
        }\n
      }\n
      return _results;\n
    })();\n
    return lines.join(\'\\n\');\n
  };\n
\n
  buildLocationData = function(first, last) {\n
    if (!last) {\n
      return first;\n
    } else {\n
      return {\n
        first_line: first.first_line,\n
        first_column: first.first_column,\n
        last_line: last.last_line,\n
        last_column: last.last_column\n
      };\n
    }\n
  };\n
\n
  exports.addLocationDataFn = function(first, last) {\n
    return function(obj) {\n
      if (((typeof obj) === \'object\') && (!!obj[\'updateLocationDataIfMissing\'])) {\n
        obj.updateLocationDataIfMissing(buildLocationData(first, last));\n
      }\n
      return obj;\n
    };\n
  };\n
\n
  exports.locationDataToString = function(obj) {\n
    var locationData;\n
    if (("2" in obj) && ("first_line" in obj[2])) {\n
      locationData = obj[2];\n
    } else if ("first_line" in obj) {\n
      locationData = obj;\n
    }\n
    if (locationData) {\n
      return ("" + (locationData.first_line + 1) + ":" + (locationData.first_column + 1) + "-") + ("" + (locationData.last_line + 1) + ":" + (locationData.last_column + 1));\n
    } else {\n
      return "No location data";\n
    }\n
  };\n
\n
  exports.baseFileName = function(file, stripExt, useWinPathSep) {\n
    var parts, pathSep;\n
    if (stripExt == null) {\n
      stripExt = false;\n
    }\n
    if (useWinPathSep == null) {\n
      useWinPathSep = false;\n
    }\n
    pathSep = useWinPathSep ? /\\\\|\\// : /\\//;\n
    parts = file.split(pathSep);\n
    file = parts[parts.length - 1];\n
    if (!stripExt) {\n
      return file;\n
    }\n
    parts = file.split(\'.\');\n
    parts.pop();\n
    if (parts[parts.length - 1] === \'coffee\' && parts.length > 1) {\n
      parts.pop();\n
    }\n
    return parts.join(\'.\');\n
  };\n
\n
  exports.isCoffee = function(file) {\n
    return /\\.((lit)?coffee|coffee\\.md)$/.test(file);\n
  };\n
\n
  exports.isLiterate = function(file) {\n
    return /\\.(litcoffee|coffee\\.md)$/.test(file);\n
  };\n
\n
  exports.throwSyntaxError = function(message, location) {\n
    var error;\n
    if (location.last_line == null) {\n
      location.last_line = location.first_line;\n
    }\n
    if (location.last_column == null) {\n
      location.last_column = location.first_column;\n
    }\n
    error = new SyntaxError(message);\n
    error.location = location;\n
    error.toString = syntaxErrorToString;\n
    error.stack = error.toString();\n
    throw error;\n
  };\n
\n
  exports.updateSyntaxError = function(error, code, filename) {\n
    if (error.toString === syntaxErrorToString) {\n
      error.code || (error.code = code);\n
      error.filename || (error.filename = filename);\n
      error.stack = error.toString();\n
    }\n
    return error;\n
  };\n
\n
  syntaxErrorToString = function() {\n
    var codeLine, colorize, colorsEnabled, end, filename, first_column, first_line, last_column, last_line, marker, start, _ref1, _ref2;\n
    if (!(this.code && this.location)) {\n
      return Error.prototype.toString.call(this);\n
    }\n
    _ref1 = this.location, first_line = _ref1.first_line, first_column = _ref1.first_column, last_line = _ref1.last_line, last_column = _ref1.last_column;\n
    if (last_line == null) {\n
      last_line = first_line;\n
    }\n
    if (last_column == null) {\n
      last_column = first_column;\n
    }\n
    filename = this.filename || \'[stdin]\';\n
    codeLine = this.code.split(\'\\n\')[first_line];\n
    start = first_column;\n
    end = first_line === last_line ? last_column + 1 : codeLine.length;\n
    marker = repeat(\' \', start) + repeat(\'^\', end - start);\n
    if (typeof process !== "undefined" && process !== null) {\n
      colorsEnabled = process.stdout.isTTY && !process.env.NODE_DISABLE_COLORS;\n
    }\n
    if ((_ref2 = this.colorful) != null ? _ref2 : colorsEnabled) {\n
      colorize = function(str) {\n
        return "\\x1B[1;31m" + str + "\\x1B[0m";\n
      };\n
      codeLine = codeLine.slice(0, start) + colorize(codeLine.slice(start, end)) + codeLine.slice(end);\n
      marker = colorize(marker);\n
    }\n
    return "" + filename + ":" + (first_line + 1) + ":" + (first_column + 1) + ": error: " + this.message + "\\n" + codeLine + "\\n" + marker;\n
  };\n
\n
\n
});\n
\n
define(\'ace/mode/coffee/parser\', [\'require\', \'exports\', \'module\' ], function(require, exports, module) {\n
\n
var parser = {trace: function trace() { },\n
yy: {},\n
symbols_: {"error":2,"Root":3,"Body":4,"Line":5,"TERMINATOR":6,"Expression":7,"Statement":8,"Return":9,"Comment":10,"STATEMENT":11,"Value":12,"Invocation":13,"Code":14,"Operation":15,"Assign":16,"If":17,"Try":18,"While":19,"For":20,"Switch":21,"Class":22,"Throw":23,"Block":24,"INDENT":25,"OUTDENT":26,"Identifier":27,"IDENTIFIER":28,"AlphaNumeric":29,"NUMBER":30,"STRING":31,"Literal":32,"JS":33,"REGEX":34,"DEBUGGER":35,"UNDEFINED":36,"NULL":37,"BOOL":38,"Assignable":39,"=":40,"AssignObj":41,"ObjAssignable":42,":":43,"ThisProperty":44,"RETURN":45,"HERECOMMENT":46,"PARAM_START":47,"ParamList":48,"PARAM_END":49,"FuncGlyph":50,"->":51,"=>":52,"OptComma":53,",":54,"Param":55,"ParamVar":56,"...":57,"Array":58,"Object":59,"Splat":60,"SimpleAssignable":61,"Accessor":62,"Parenthetical":63,"Range":64,"This":65,".":66,"?.":67,"::":68,"?::":69,"Index":70,"INDEX_START":71,"IndexValue":72,"INDEX_END":73,"INDEX_SOAK":74,"Slice":75,"{":76,"AssignList":77,"}":78,"CLASS":79,"EXTENDS":80,"OptFuncExist":81,"Arguments":82,"SUPER":83,"FUNC_EXIST":84,"CALL_START":85,"CALL_END":86,"ArgList":87,"THIS":88,"@":89,"[":90,"]":91,"RangeDots":92,"..":93,"Arg":94,"SimpleArgs":95,"TRY":96,"Catch":97,"FINALLY":98,"CATCH":99,"THROW":100,"(":101,")":102,"WhileSource":103,"WHILE":104,"WHEN":105,"UNTIL":106,"Loop":107,"LOOP":108,"ForBody":109,"FOR":110,"ForStart":111,"ForSource":112,"ForVariables":113,"OWN":114,"ForValue":115,"FORIN":116,"FOROF":117,"BY":118,"SWITCH":119,"Whens":120,"ELSE":121,"When":122,"LEADING_WHEN":123,"IfBlock":124,"IF":125,"POST_IF":126,"UNARY":127,"-":128,"+":129,"--":130,"++":131,"?":132,"MATH":133,"SHIFT":134,"COMPARE":135,"LOGIC":136,"RELATION":137,"COMPOUND_ASSIGN":138,"$accept":0,"$end":1},\n
terminals_: {2:"error",6:"TERMINATOR",11:"STATEMENT",25:"INDENT",26:"OUTDENT",28:"IDENTIFIER",30:"NUMBER",31:"STRING",33:"JS",34:"REGEX",35:"DEBUGGER",36:"UNDEFINED",37:"NULL",38:"BOOL",40:"=",43:":",45:"RETURN",46:"HERECOMMENT",47:"PARAM_START",49:"PARAM_END",51:"->",52:"=>",54:",",57:"...",66:".",67:"?.",68:"::",69:"?::",71:"INDEX_START",73:"INDEX_END",74:"INDEX_SOAK",76:"{",78:"}",79:"CLASS",80:"EXTENDS",83:"SUPER",84:"FUNC_EXIST",85:"CALL_START",86:"CALL_END",88:"THIS",89:"@",90:"[",91:"]",93:"..",96:"TRY",98:"FINALLY",99:"CATCH",100:"THROW",101:"(",102:")",104:"WHILE",105:"WHEN",106:"UNTIL",108:"LOOP",110:"FOR",114:"OWN",116:"FORIN",117:"FOROF",118:"BY",119:"SWITCH",121:"ELSE",123:"LEADING_WHEN",125:"IF",126:"POST_IF",127:"UNARY",128:"-",129:"+",130:"--",131:"++",132:"?",133:"MATH",134:"SHIFT",135:"COMPARE",136:"LOGIC",137:"RELATION",138:"COMPOUND_ASSIGN"},\n
productions_: [0,[3,0],[3,1],[4,1],[4,3],[4,2],[5,1],[5,1],[8,1],[8,1],[8,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[7,1],[24,2],[24,3],[27,1],[29,1],[29,1],[32,1],[32,1],[32,1],[32,1],[32,1],[32,1],[32,1],[16,3],[16,4],[16,5],[41,1],[41,3],[41,5],[41,1],[42,1],[42,1],[42,1],[9,2],[9,1],[10,1],[14,5],[14,2],[50,1],[50,1],[53,0],[53,1],[48,0],[48,1],[48,3],[48,4],[48,6],[55,1],[55,2],[55,3],[56,1],[56,1],[56,1],[56,1],[60,2],[61,1],[61,2],[61,2],[61,1],[39,1],[39,1],[39,1],[12,1],[12,1],[12,1],[12,1],[12,1],[62,2],[62,2],[62,2],[62,2],[62,1],[62,1],[70,3],[70,2],[72,1],[72,1],[59,4],[77,0],[77,1],[77,3],[77,4],[77,6],[22,1],[22,2],[22,3],[22,4],[22,2],[22,3],[22,4],[22,5],[13,3],[13,3],[13,1],[13,2],[81,0],[81,1],[82,2],[82,4],[65,1],[65,1],[44,2],[58,2],[58,4],[92,1],[92,1],[64,5],[75,3],[75,2],[75,2],[75,1],[87,1],[87,3],[87,4],[87,4],[87,6],[94,1],[94,1],[95,1],[95,3],[18,2],[18,3],[18,4],[18,5],[97,3],[97,3],[97,2],[23,2],[63,3],[63,5],[103,2],[103,4],[103,2],[103,4],[19,2],[19,2],[19,2],[19,1],[107,2],[107,2],[20,2],[20,2],[20,2],[109,2],[109,2],[111,2],[111,3],[115,1],[115,1],[115,1],[115,1],[113,1],[113,3],[112,2],[112,2],[112,4],[112,4],[112,4],[112,6],[112,6],[21,5],[21,7],[21,4],[21,6],[120,1],[120,2],[122,3],[122,4],[124,3],[124,5],[17,1],[17,3],[17,3],[17,3],[15,2],[15,2],[15,2],[15,2],[15,2],[15,2],[15,2],[15,2],[15,3],[15,3],[15,3],[15,3],[15,3],[15,3],[15,3],[15,3],[15,5],[15,4],[15,3]],\n
performAction: function anonymous(yytext, yyleng, yylineno, yy, yystate /* action[1] */, $$ /* vstack */, _$ /* lstack */) {\n
\n
var $0 = $$.length - 1;\n
switch (yystate) {\n
case 1:return this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Block);\n
break;\n
case 2:return this.$ = $$[$0];\n
break;\n
case 3:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(yy.Block.wrap([$$[$0]]));\n
break;\n
case 4:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-2].push($$[$0]));\n
break;\n
case 5:this.$ = $$[$0-1];\n
break;\n
case 6:this.$ = $$[$0];\n
break;\n
case 7:this.$ = $$[$0];\n
break;\n
case 8:this.$ = $$[$0];\n
break;\n
case 9:this.$ = $$[$0];\n
break;\n
case 10:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 11:this.$ = $$[$0];\n
break;\n
case 12:this.$ = $$[$0];\n
break;\n
case 13:this.$ = $$[$0];\n
break;\n
case 14:this.$ = $$[$0];\n
break;\n
case 15:this.$ = $$[$0];\n
break;\n
case 16:this.$ = $$[$0];\n
break;\n
case 17:this.$ = $$[$0];\n
break;\n
case 18:this.$ = $$[$0];\n
break;\n
case 19:this.$ = $$[$0];\n
break;\n
case 20:this.$ = $$[$0];\n
break;\n
case 21:this.$ = $$[$0];\n
break;\n
case 22:this.$ = $$[$0];\n
break;\n
case 23:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Block);\n
break;\n
case 24:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-1]);\n
break;\n
case 25:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 26:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 27:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 28:this.$ = $$[$0];\n
break;\n
case 29:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 30:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 31:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Literal($$[$0]));\n
break;\n
case 32:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Undefined);\n
break;\n
case 33:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Null);\n
break;\n
case 34:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Bool($$[$0]));\n
break;\n
case 35:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Assign($$[$0-2], $$[$0]));\n
break;\n
case 36:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Assign($$[$0-3], $$[$0]));\n
break;\n
case 37:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Assign($$[$0-4], $$[$0-1]));\n
break;\n
case 38:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 39:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Assign(yy.addLocationDataFn(_$[$0-2])(new yy.Value($$[$0-2])), $$[$0], \'object\'));\n
break;\n
case 40:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Assign(yy.addLocationDataFn(_$[$0-4])(new yy.Value($$[$0-4])), $$[$0-1], \'object\'));\n
break;\n
case 41:this.$ = $$[$0];\n
break;\n
case 42:this.$ = $$[$0];\n
break;\n
case 43:this.$ = $$[$0];\n
break;\n
case 44:this.$ = $$[$0];\n
break;\n
case 45:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Return($$[$0]));\n
break;\n
case 46:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Return);\n
break;\n
case 47:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Comment($$[$0]));\n
break;\n
case 48:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Code($$[$0-3], $$[$0], $$[$0-1]));\n
break;\n
case 49:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Code([], $$[$0], $$[$0-1]));\n
break;\n
case 50:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(\'func\');\n
break;\n
case 51:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(\'boundfunc\');\n
break;\n
case 52:this.$ = $$[$0];\n
break;\n
case 53:this.$ = $$[$0];\n
break;\n
case 54:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])([]);\n
break;\n
case 55:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])([$$[$0]]);\n
break;\n
case 56:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-2].concat($$[$0]));\n
break;\n
case 57:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])($$[$0-3].concat($$[$0]));\n
break;\n
case 58:this.$ = yy.addLocationDataFn(_$[$0-5], _$[$0])($$[$0-5].concat($$[$0-2]));\n
break;\n
case 59:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Param($$[$0]));\n
break;\n
case 60:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Param($$[$0-1], null, true));\n
break;\n
case 61:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Param($$[$0-2], $$[$0]));\n
break;\n
case 62:this.$ = $$[$0];\n
break;\n
case 63:this.$ = $$[$0];\n
break;\n
case 64:this.$ = $$[$0];\n
break;\n
case 65:this.$ = $$[$0];\n
break;\n
case 66:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Splat($$[$0-1]));\n
break;\n
case 67:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 68:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])($$[$0-1].add($$[$0]));\n
break;\n
case 69:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Value($$[$0-1], [].concat($$[$0])));\n
break;\n
case 70:this.$ = $$[$0];\n
break;\n
case 71:this.$ = $$[$0];\n
break;\n
case 72:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 73:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 74:this.$ = $$[$0];\n
break;\n
case 75:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 76:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 77:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 78:this.$ = $$[$0];\n
break;\n
case 79:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Access($$[$0]));\n
break;\n
case 80:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Access($$[$0], \'soak\'));\n
break;\n
case 81:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])([yy.addLocationDataFn(_$[$0-1])(new yy.Access(new yy.Literal(\'prototype\'))), yy.addLocationDataFn(_$[$0])(new yy.Access($$[$0]))]);\n
break;\n
case 82:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])([yy.addLocationDataFn(_$[$0-1])(new yy.Access(new yy.Literal(\'prototype\'), \'soak\')), yy.addLocationDataFn(_$[$0])(new yy.Access($$[$0]))]);\n
break;\n
case 83:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Access(new yy.Literal(\'prototype\')));\n
break;\n
case 84:this.$ = $$[$0];\n
break;\n
case 85:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-1]);\n
break;\n
case 86:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(yy.extend($$[$0], {\n
          soak: true\n
        }));\n
break;\n
case 87:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Index($$[$0]));\n
break;\n
case 88:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Slice($$[$0]));\n
break;\n
case 89:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Obj($$[$0-2], $$[$0-3].generated));\n
break;\n
case 90:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])([]);\n
break;\n
case 91:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])([$$[$0]]);\n
break;\n
case 92:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-2].concat($$[$0]));\n
break;\n
case 93:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])($$[$0-3].concat($$[$0]));\n
break;\n
case 94:this.$ = yy.addLocationDataFn(_$[$0-5], _$[$0])($$[$0-5].concat($$[$0-2]));\n
break;\n
case 95:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Class);\n
break;\n
case 96:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Class(null, null, $$[$0]));\n
break;\n
case 97:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Class(null, $$[$0]));\n
break;\n
case 98:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Class(null, $$[$0-1], $$[$0]));\n
break;\n
case 99:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Class($$[$0]));\n
break;\n
case 100:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Class($$[$0-1], null, $$[$0]));\n
break;\n
case 101:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Class($$[$0-2], $$[$0]));\n
break;\n
case 102:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Class($$[$0-3], $$[$0-1], $$[$0]));\n
break;\n
case 103:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Call($$[$0-2], $$[$0], $$[$0-1]));\n
break;\n
case 104:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Call($$[$0-2], $$[$0], $$[$0-1]));\n
break;\n
case 105:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Call(\'super\', [new yy.Splat(new yy.Literal(\'arguments\'))]));\n
break;\n
case 106:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Call(\'super\', $$[$0]));\n
break;\n
case 107:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(false);\n
break;\n
case 108:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(true);\n
break;\n
case 109:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])([]);\n
break;\n
case 110:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])($$[$0-2]);\n
break;\n
case 111:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value(new yy.Literal(\'this\')));\n
break;\n
case 112:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value(new yy.Literal(\'this\')));\n
break;\n
case 113:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Value(yy.addLocationDataFn(_$[$0-1])(new yy.Literal(\'this\')), [yy.addLocationDataFn(_$[$0])(new yy.Access($$[$0]))], \'this\'));\n
break;\n
case 114:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Arr([]));\n
break;\n
case 115:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Arr($$[$0-2]));\n
break;\n
case 116:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(\'inclusive\');\n
break;\n
case 117:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(\'exclusive\');\n
break;\n
case 118:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Range($$[$0-3], $$[$0-1], $$[$0-2]));\n
break;\n
case 119:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Range($$[$0-2], $$[$0], $$[$0-1]));\n
break;\n
case 120:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Range($$[$0-1], null, $$[$0]));\n
break;\n
case 121:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Range(null, $$[$0], $$[$0-1]));\n
break;\n
case 122:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Range(null, null, $$[$0]));\n
break;\n
case 123:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])([$$[$0]]);\n
break;\n
case 124:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-2].concat($$[$0]));\n
break;\n
case 125:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])($$[$0-3].concat($$[$0]));\n
break;\n
case 126:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])($$[$0-2]);\n
break;\n
case 127:this.$ = yy.addLocationDataFn(_$[$0-5], _$[$0])($$[$0-5].concat($$[$0-2]));\n
break;\n
case 128:this.$ = $$[$0];\n
break;\n
case 129:this.$ = $$[$0];\n
break;\n
case 130:this.$ = $$[$0];\n
break;\n
case 131:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])([].concat($$[$0-2], $$[$0]));\n
break;\n
case 132:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Try($$[$0]));\n
break;\n
case 133:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Try($$[$0-1], $$[$0][0], $$[$0][1]));\n
break;\n
case 134:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Try($$[$0-2], null, null, $$[$0]));\n
break;\n
case 135:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Try($$[$0-3], $$[$0-2][0], $$[$0-2][1], $$[$0]));\n
break;\n
case 136:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])([$$[$0-1], $$[$0]]);\n
break;\n
case 137:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])([yy.addLocationDataFn(_$[$0-1])(new yy.Value($$[$0-1])), $$[$0]]);\n
break;\n
case 138:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])([null, $$[$0]]);\n
break;\n
case 139:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Throw($$[$0]));\n
break;\n
case 140:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Parens($$[$0-1]));\n
break;\n
case 141:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Parens($$[$0-2]));\n
break;\n
case 142:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.While($$[$0]));\n
break;\n
case 143:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.While($$[$0-2], {\n
          guard: $$[$0]\n
        }));\n
break;\n
case 144:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.While($$[$0], {\n
          invert: true\n
        }));\n
break;\n
case 145:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.While($$[$0-2], {\n
          invert: true,\n
          guard: $$[$0]\n
        }));\n
break;\n
case 146:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])($$[$0-1].addBody($$[$0]));\n
break;\n
case 147:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])($$[$0].addBody(yy.addLocationDataFn(_$[$0-1])(yy.Block.wrap([$$[$0-1]]))));\n
break;\n
case 148:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])($$[$0].addBody(yy.addLocationDataFn(_$[$0-1])(yy.Block.wrap([$$[$0-1]]))));\n
break;\n
case 149:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])($$[$0]);\n
break;\n
case 150:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.While(yy.addLocationDataFn(_$[$0-1])(new yy.Literal(\'true\'))).addBody($$[$0]));\n
break;\n
case 151:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.While(yy.addLocationDataFn(_$[$0-1])(new yy.Literal(\'true\'))).addBody(yy.addLocationDataFn(_$[$0])(yy.Block.wrap([$$[$0]]))));\n
break;\n
case 152:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.For($$[$0-1], $$[$0]));\n
break;\n
case 153:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.For($$[$0-1], $$[$0]));\n
break;\n
case 154:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.For($$[$0], $$[$0-1]));\n
break;\n
case 155:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])({\n
          source: yy.addLocationDataFn(_$[$0])(new yy.Value($$[$0]))\n
        });\n
break;\n
case 156:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])((function () {\n
        $$[$0].own = $$[$0-1].own;\n
        $$[$0].name = $$[$0-1][0];\n
        $$[$0].index = $$[$0-1][1];\n
        return $$[$0];\n
      }()));\n
break;\n
case 157:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])($$[$0]);\n
break;\n
case 158:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])((function () {\n
        $$[$0].own = true;\n
        return $$[$0];\n
      }()));\n
break;\n
case 159:this.$ = $$[$0];\n
break;\n
case 160:this.$ = $$[$0];\n
break;\n
case 161:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 162:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])(new yy.Value($$[$0]));\n
break;\n
case 163:this.$ = yy.addLocationDataFn(_$[$0], _$[$0])([$$[$0]]);\n
break;\n
case 164:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])([$$[$0-2], $$[$0]]);\n
break;\n
case 165:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])({\n
          source: $$[$0]\n
        });\n
break;\n
case 166:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])({\n
          source: $$[$0],\n
          object: true\n
        });\n
break;\n
case 167:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])({\n
          source: $$[$0-2],\n
          guard: $$[$0]\n
        });\n
break;\n
case 168:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])({\n
          source: $$[$0-2],\n
          guard: $$[$0],\n
          object: true\n
        });\n
break;\n
case 169:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])({\n
          source: $$[$0-2],\n
          step: $$[$0]\n
        });\n
break;\n
case 170:this.$ = yy.addLocationDataFn(_$[$0-5], _$[$0])({\n
          source: $$[$0-4],\n
          guard: $$[$0-2],\n
          step: $$[$0]\n
        });\n
break;\n
case 171:this.$ = yy.addLocationDataFn(_$[$0-5], _$[$0])({\n
          source: $$[$0-4],\n
          step: $$[$0-2],\n
          guard: $$[$0]\n
        });\n
break;\n
case 172:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Switch($$[$0-3], $$[$0-1]));\n
break;\n
case 173:this.$ = yy.addLocationDataFn(_$[$0-6], _$[$0])(new yy.Switch($$[$0-5], $$[$0-3], $$[$0-1]));\n
break;\n
case 174:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Switch(null, $$[$0-1]));\n
break;\n
case 175:this.$ = yy.addLocationDataFn(_$[$0-5], _$[$0])(new yy.Switch(null, $$[$0-3], $$[$0-1]));\n
break;\n
case 176:this.$ = $$[$0];\n
break;\n
case 177:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])($$[$0-1].concat($$[$0]));\n
break;\n
case 178:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])([[$$[$0-1], $$[$0]]]);\n
break;\n
case 179:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])([[$$[$0-2], $$[$0-1]]]);\n
break;\n
case 180:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.If($$[$0-1], $$[$0], {\n
          type: $$[$0-2]\n
        }));\n
break;\n
case 181:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])($$[$0-4].addElse(yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.If($$[$0-1], $$[$0], {\n
          type: $$[$0-2]\n
        }))));\n
break;\n
case 182:this.$ = $$[$0];\n
break;\n
case 183:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])($$[$0-2].addElse($$[$0]));\n
break;\n
case 184:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.If($$[$0], yy.addLocationDataFn(_$[$0-2])(yy.Block.wrap([$$[$0-2]])), {\n
          type: $$[$0-1],\n
          statement: true\n
        }));\n
break;\n
case 185:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.If($$[$0], yy.addLocationDataFn(_$[$0-2])(yy.Block.wrap([$$[$0-2]])), {\n
          type: $$[$0-1],\n
          statement: true\n
        }));\n
break;\n
case 186:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op($$[$0-1], $$[$0]));\n
break;\n
case 187:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op(\'-\', $$[$0]));\n
break;\n
case 188:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op(\'+\', $$[$0]));\n
break;\n
case 189:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op(\'--\', $$[$0]));\n
break;\n
case 190:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op(\'++\', $$[$0]));\n
break;\n
case 191:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op(\'--\', $$[$0-1], null, true));\n
break;\n
case 192:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Op(\'++\', $$[$0-1], null, true));\n
break;\n
case 193:this.$ = yy.addLocationDataFn(_$[$0-1], _$[$0])(new yy.Existence($$[$0-1]));\n
break;\n
case 194:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Op(\'+\', $$[$0-2], $$[$0]));\n
break;\n
case 195:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Op(\'-\', $$[$0-2], $$[$0]));\n
break;\n
case 196:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Op($$[$0-1], $$[$0-2], $$[$0]));\n
break;\n
case 197:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Op($$[$0-1], $$[$0-2], $$[$0]));\n
break;\n
case 198:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Op($$[$0-1], $$[$0-2], $$[$0]));\n
break;\n
case 199:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Op($$[$0-1], $$[$0-2], $$[$0]));\n
break;\n
case 200:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])((function () {\n
        if ($$[$0-1].charAt(0) === \'!\') {\n
          return new yy.Op($$[$0-1].slice(1), $$[$0-2], $$[$0]).invert();\n
        } else {\n
          return new yy.Op($$[$0-1], $$[$0-2], $$[$0]);\n
        }\n
      }()));\n
break;\n
case 201:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Assign($$[$0-2], $$[$0], $$[$0-1]));\n
break;\n
case 202:this.$ = yy.addLocationDataFn(_$[$0-4], _$[$0])(new yy.Assign($$[$0-4], $$[$0-1], $$[$0-3]));\n
break;\n
case 203:this.$ = yy.addLocationDataFn(_$[$0-3], _$[$0])(new yy.Assign($$[$0-3], $$[$0], $$[$0-2]));\n
break;\n
case 204:this.$ = yy.addLocationDataFn(_$[$0-2], _$[$0])(new yy.Extends($$[$0-2], $$[$0]));\n
break;\n
}\n
},\n
table: [{1:[2,1],3:1,4:2,5:3,7:4,8:5,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[3]},{1:[2,2],6:[1,72]},{1:[2,3],6:[2,3],26:[2,3],102:[2,3]},{1:[2,6],6:[2,6],26:[2,6],102:[2,6],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,7],6:[2,7],26:[2,7],102:[2,7],103:85,104:[1,63],106:[1,64],109:86,110:[1,66],111:67,126:[1,84]},{1:[2,11],6:[2,11],25:[2,11],26:[2,11],49:[2,11],54:[2,11],57:[2,11],62:88,66:[1,90],67:[1,91],68:[1,92],69:[1,93],70:94,71:[1,95],73:[2,11],74:[1,96],78:[2,11],81:87,84:[1,89],85:[2,107],86:[2,11],91:[2,11],93:[2,11],102:[2,11],104:[2,11],105:[2,11],106:[2,11],110:[2,11],118:[2,11],126:[2,11],128:[2,11],129:[2,11],132:[2,11],133:[2,11],134:[2,11],135:[2,11],136:[2,11],137:[2,11]},{1:[2,12],6:[2,12],25:[2,12],26:[2,12],49:[2,12],54:[2,12],57:[2,12],62:98,66:[1,90],67:[1,91],68:[1,92],69:[1,93],70:94,71:[1,95],73:[2,12],74:[1,96],78:[2,12],81:97,84:[1,89],85:[2,107],86:[2,12],91:[2,12],93:[2,12],102:[2,12],104:[2,12],105:[2,12],106:[2,12],110:[2,12],118:[2,12],126:[2,12],128:[2,12],129:[2,12],132:[2,12],133:[2,12],134:[2,12],135:[2,12],136:[2,12],137:[2,12]},{1:[2,13],6:[2,13],25:[2,13],26:[2,13],49:[2,13],54:[2,13],57:[2,13],73:[2,13],78:[2,13],86:[2,13],91:[2,13],93:[2,13],102:[2,13],104:[2,13],105:[2,13],106:[2,13],110:[2,13],118:[2,13],126:[2,13],128:[2,13],129:[2,13],132:[2,13],133:[2,13],134:[2,13],135:[2,13],136:[2,13],137:[2,13]},{1:[2,14],6:[2,14],25:[2,14],26:[2,14],49:[2,14],54:[2,14],57:[2,14],73:[2,14],78:[2,14],86:[2,14],91:[2,14],93:[2,14],102:[2,14],104:[2,14],105:[2,14],106:[2,14],110:[2,14],118:[2,14],126:[2,14],128:[2,14],129:[2,14],132:[2,14],133:[2,14],134:[2,14],135:[2,14],136:[2,14],137:[2,14]},{1:[2,15],6:[2,15],25:[2,15],26:[2,15],49:[2,15],54:[2,15],57:[2,15],73:[2,15],78:[2,15],86:[2,15],91:[2,15],93:[2,15],102:[2,15],104:[2,15],105:[2,15],106:[2,15],110:[2,15],118:[2,15],126:[2,15],128:[2,15],129:[2,15],132:[2,15],133:[2,15],134:[2,15],135:[2,15],136:[2,15],137:[2,15]},{1:[2,16],6:[2,16],25:[2,16],26:[2,16],49:[2,16],54:[2,16],57:[2,16],73:[2,16],78:[2,16],86:[2,16],91:[2,16],93:[2,16],102:[2,16],104:[2,16],105:[2,16],106:[2,16],110:[2,16],118:[2,16],126:[2,16],128:[2,16],129:[2,16],132:[2,16],133:[2,16],134:[2,16],135:[2,16],136:[2,16],137:[2,16]},{1:[2,17],6:[2,17],25:[2,17],26:[2,17],49:[2,17],54:[2,17],57:[2,17],73:[2,17],78:[2,17],86:[2,17],91:[2,17],93:[2,17],102:[2,17],104:[2,17],105:[2,17],106:[2,17],110:[2,17],118:[2,17],126:[2,17],128:[2,17],129:[2,17],132:[2,17],133:[2,17],134:[2,17],

]]></string> </value>
        </item>
        <item>
            <key> <string>next</string> </key>
            <value>
              <persistent> <string encoding="base64">AAAAAAAAAAQ=</string> </persistent>
            </value>
        </item>
      </dictionary>
    </pickle>
  </record>
  <record id="4" aka="AAAAAAAAAAQ=">
    <pickle>
      <global name="Pdata" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>data</string> </key>
            <value> <string>135:[2,17],136:[2,17],137:[2,17]},{1:[2,18],6:[2,18],25:[2,18],26:[2,18],49:[2,18],54:[2,18],57:[2,18],73:[2,18],78:[2,18],86:[2,18],91:[2,18],93:[2,18],102:[2,18],104:[2,18],105:[2,18],106:[2,18],110:[2,18],118:[2,18],126:[2,18],128:[2,18],129:[2,18],132:[2,18],133:[2,18],134:[2,18],135:[2,18],136:[2,18],137:[2,18]},{1:[2,19],6:[2,19],25:[2,19],26:[2,19],49:[2,19],54:[2,19],57:[2,19],73:[2,19],78:[2,19],86:[2,19],91:[2,19],93:[2,19],102:[2,19],104:[2,19],105:[2,19],106:[2,19],110:[2,19],118:[2,19],126:[2,19],128:[2,19],129:[2,19],132:[2,19],133:[2,19],134:[2,19],135:[2,19],136:[2,19],137:[2,19]},{1:[2,20],6:[2,20],25:[2,20],26:[2,20],49:[2,20],54:[2,20],57:[2,20],73:[2,20],78:[2,20],86:[2,20],91:[2,20],93:[2,20],102:[2,20],104:[2,20],105:[2,20],106:[2,20],110:[2,20],118:[2,20],126:[2,20],128:[2,20],129:[2,20],132:[2,20],133:[2,20],134:[2,20],135:[2,20],136:[2,20],137:[2,20]},{1:[2,21],6:[2,21],25:[2,21],26:[2,21],49:[2,21],54:[2,21],57:[2,21],73:[2,21],78:[2,21],86:[2,21],91:[2,21],93:[2,21],102:[2,21],104:[2,21],105:[2,21],106:[2,21],110:[2,21],118:[2,21],126:[2,21],128:[2,21],129:[2,21],132:[2,21],133:[2,21],134:[2,21],135:[2,21],136:[2,21],137:[2,21]},{1:[2,22],6:[2,22],25:[2,22],26:[2,22],49:[2,22],54:[2,22],57:[2,22],73:[2,22],78:[2,22],86:[2,22],91:[2,22],93:[2,22],102:[2,22],104:[2,22],105:[2,22],106:[2,22],110:[2,22],118:[2,22],126:[2,22],128:[2,22],129:[2,22],132:[2,22],133:[2,22],134:[2,22],135:[2,22],136:[2,22],137:[2,22]},{1:[2,8],6:[2,8],26:[2,8],102:[2,8],104:[2,8],106:[2,8],110:[2,8],126:[2,8]},{1:[2,9],6:[2,9],26:[2,9],102:[2,9],104:[2,9],106:[2,9],110:[2,9],126:[2,9]},{1:[2,10],6:[2,10],26:[2,10],102:[2,10],104:[2,10],106:[2,10],110:[2,10],126:[2,10]},{1:[2,74],6:[2,74],25:[2,74],26:[2,74],40:[1,99],49:[2,74],54:[2,74],57:[2,74],66:[2,74],67:[2,74],68:[2,74],69:[2,74],71:[2,74],73:[2,74],74:[2,74],78:[2,74],84:[2,74],85:[2,74],86:[2,74],91:[2,74],93:[2,74],102:[2,74],104:[2,74],105:[2,74],106:[2,74],110:[2,74],118:[2,74],126:[2,74],128:[2,74],129:[2,74],132:[2,74],133:[2,74],134:[2,74],135:[2,74],136:[2,74],137:[2,74]},{1:[2,75],6:[2,75],25:[2,75],26:[2,75],49:[2,75],54:[2,75],57:[2,75],66:[2,75],67:[2,75],68:[2,75],69:[2,75],71:[2,75],73:[2,75],74:[2,75],78:[2,75],84:[2,75],85:[2,75],86:[2,75],91:[2,75],93:[2,75],102:[2,75],104:[2,75],105:[2,75],106:[2,75],110:[2,75],118:[2,75],126:[2,75],128:[2,75],129:[2,75],132:[2,75],133:[2,75],134:[2,75],135:[2,75],136:[2,75],137:[2,75]},{1:[2,76],6:[2,76],25:[2,76],26:[2,76],49:[2,76],54:[2,76],57:[2,76],66:[2,76],67:[2,76],68:[2,76],69:[2,76],71:[2,76],73:[2,76],74:[2,76],78:[2,76],84:[2,76],85:[2,76],86:[2,76],91:[2,76],93:[2,76],102:[2,76],104:[2,76],105:[2,76],106:[2,76],110:[2,76],118:[2,76],126:[2,76],128:[2,76],129:[2,76],132:[2,76],133:[2,76],134:[2,76],135:[2,76],136:[2,76],137:[2,76]},{1:[2,77],6:[2,77],25:[2,77],26:[2,77],49:[2,77],54:[2,77],57:[2,77],66:[2,77],67:[2,77],68:[2,77],69:[2,77],71:[2,77],73:[2,77],74:[2,77],78:[2,77],84:[2,77],85:[2,77],86:[2,77],91:[2,77],93:[2,77],102:[2,77],104:[2,77],105:[2,77],106:[2,77],110:[2,77],118:[2,77],126:[2,77],128:[2,77],129:[2,77],132:[2,77],133:[2,77],134:[2,77],135:[2,77],136:[2,77],137:[2,77]},{1:[2,78],6:[2,78],25:[2,78],26:[2,78],49:[2,78],54:[2,78],57:[2,78],66:[2,78],67:[2,78],68:[2,78],69:[2,78],71:[2,78],73:[2,78],74:[2,78],78:[2,78],84:[2,78],85:[2,78],86:[2,78],91:[2,78],93:[2,78],102:[2,78],104:[2,78],105:[2,78],106:[2,78],110:[2,78],118:[2,78],126:[2,78],128:[2,78],129:[2,78],132:[2,78],133:[2,78],134:[2,78],135:[2,78],136:[2,78],137:[2,78]},{1:[2,105],6:[2,105],25:[2,105],26:[2,105],49:[2,105],54:[2,105],57:[2,105],66:[2,105],67:[2,105],68:[2,105],69:[2,105],71:[2,105],73:[2,105],74:[2,105],78:[2,105],82:100,84:[2,105],85:[1,101],86:[2,105],91:[2,105],93:[2,105],102:[2,105],104:[2,105],105:[2,105],106:[2,105],110:[2,105],118:[2,105],126:[2,105],128:[2,105],129:[2,105],132:[2,105],133:[2,105],134:[2,105],135:[2,105],136:[2,105],137:[2,105]},{6:[2,54],25:[2,54],27:105,28:[1,71],44:106,48:102,49:[2,54],54:[2,54],55:103,56:104,58:107,59:108,76:[1,68],89:[1,109],90:[1,110]},{24:111,25:[1,112]},{7:113,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:115,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:116,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{12:118,13:119,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:120,44:61,58:45,59:46,61:117,63:23,64:24,65:25,76:[1,68],83:[1,26],88:[1,56],89:[1,57],90:[1,55],101:[1,54]},{12:118,13:119,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:120,44:61,58:45,59:46,61:121,63:23,64:24,65:25,76:[1,68],83:[1,26],88:[1,56],89:[1,57],90:[1,55],101:[1,54]},{1:[2,71],6:[2,71],25:[2,71],26:[2,71],40:[2,71],49:[2,71],54:[2,71],57:[2,71],66:[2,71],67:[2,71],68:[2,71],69:[2,71],71:[2,71],73:[2,71],74:[2,71],78:[2,71],80:[1,125],84:[2,71],85:[2,71],86:[2,71],91:[2,71],93:[2,71],102:[2,71],104:[2,71],105:[2,71],106:[2,71],110:[2,71],118:[2,71],126:[2,71],128:[2,71],129:[2,71],130:[1,122],131:[1,123],132:[2,71],133:[2,71],134:[2,71],135:[2,71],136:[2,71],137:[2,71],138:[1,124]},{1:[2,182],6:[2,182],25:[2,182],26:[2,182],49:[2,182],54:[2,182],57:[2,182],73:[2,182],78:[2,182],86:[2,182],91:[2,182],93:[2,182],102:[2,182],104:[2,182],105:[2,182],106:[2,182],110:[2,182],118:[2,182],121:[1,126],126:[2,182],128:[2,182],129:[2,182],132:[2,182],133:[2,182],134:[2,182],135:[2,182],136:[2,182],137:[2,182]},{24:127,25:[1,112]},{24:128,25:[1,112]},{1:[2,149],6:[2,149],25:[2,149],26:[2,149],49:[2,149],54:[2,149],57:[2,149],73:[2,149],78:[2,149],86:[2,149],91:[2,149],93:[2,149],102:[2,149],104:[2,149],105:[2,149],106:[2,149],110:[2,149],118:[2,149],126:[2,149],128:[2,149],129:[2,149],132:[2,149],133:[2,149],134:[2,149],135:[2,149],136:[2,149],137:[2,149]},{24:129,25:[1,112]},{7:130,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,131],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,95],6:[2,95],12:118,13:119,24:132,25:[1,112],26:[2,95],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:120,44:61,49:[2,95],54:[2,95],57:[2,95],58:45,59:46,61:134,63:23,64:24,65:25,73:[2,95],76:[1,68],78:[2,95],80:[1,133],83:[1,26],86:[2,95],88:[1,56],89:[1,57],90:[1,55],91:[2,95],93:[2,95],101:[1,54],102:[2,95],104:[2,95],105:[2,95],106:[2,95],110:[2,95],118:[2,95],126:[2,95],128:[2,95],129:[2,95],132:[2,95],133:[2,95],134:[2,95],135:[2,95],136:[2,95],137:[2,95]},{7:135,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,46],6:[2,46],7:136,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,26:[2,46],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],102:[2,46],103:37,104:[2,46],106:[2,46],107:38,108:[1,65],109:39,110:[2,46],111:67,119:[1,40],124:35,125:[1,62],126:[2,46],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,47],6:[2,47],25:[2,47],26:[2,47],54:[2,47],78:[2,47],102:[2,47],104:[2,47],106:[2,47],110:[2,47],126:[2,47]},{1:[2,72],6:[2,72],25:[2,72],26:[2,72],40:[2,72],49:[2,72],54:[2,72],57:[2,72],66:[2,72],67:[2,72],68:[2,72],69:[2,72],71:[2,72],73:[2,72],74:[2,72],78:[2,72],84:[2,72],85:[2,72],86:[2,72],91:[2,72],93:[2,72],102:[2,72],104:[2,72],105:[2,72],106:[2,72],110:[2,72],118:[2,72],126:[2,72],128:[2,72],129:[2,72],132:[2,72],133:[2,72],134:[2,72],135:[2,72],136:[2,72],137:[2,72]},{1:[2,73],6:[2,73],25:[2,73],26:[2,73],40:[2,73],49:[2,73],54:[2,73],57:[2,73],66:[2,73],67:[2,73],68:[2,73],69:[2,73],71:[2,73],73:[2,73],74:[2,73],78:[2,73],84:[2,73],85:[2,73],86:[2,73],91:[2,73],93:[2,73],102:[2,73],104:[2,73],105:[2,73],106:[2,73],110:[2,73],118:[2,73],126:[2,73],128:[2,73],129:[2,73],132:[2,73],133:[2,73],134:[2,73],135:[2,73],136:[2,73],137:[2,73]},{1:[2,28],6:[2,28],25:[2,28],26:[2,28],49:[2,28],54:[2,28],57:[2,28],66:[2,28],67:[2,28],68:[2,28],69:[2,28],71:[2,28],73:[2,28],74:[2,28],78:[2,28],84:[2,28],85:[2,28],86:[2,28],91:[2,28],93:[2,28],102:[2,28],104:[2,28],105:[2,28],106:[2,28],110:[2,28],118:[2,28],126:[2,28],128:[2,28],129:[2,28],132:[2,28],133:[2,28],134:[2,28],135:[2,28],136:[2,28],137:[2,28]},{1:[2,29],6:[2,29],25:[2,29],26:[2,29],49:[2,29],54:[2,29],57:[2,29],66:[2,29],67:[2,29],68:[2,29],69:[2,29],71:[2,29],73:[2,29],74:[2,29],78:[2,29],84:[2,29],85:[2,29],86:[2,29],91:[2,29],93:[2,29],102:[2,29],104:[2,29],105:[2,29],106:[2,29],110:[2,29],118:[2,29],126:[2,29],128:[2,29],129:[2,29],132:[2,29],133:[2,29],134:[2,29],135:[2,29],136:[2,29],137:[2,29]},{1:[2,30],6:[2,30],25:[2,30],26:[2,30],49:[2,30],54:[2,30],57:[2,30],66:[2,30],67:[2,30],68:[2,30],69:[2,30],71:[2,30],73:[2,30],74:[2,30],78:[2,30],84:[2,30],85:[2,30],86:[2,30],91:[2,30],93:[2,30],102:[2,30],104:[2,30],105:[2,30],106:[2,30],110:[2,30],118:[2,30],126:[2,30],128:[2,30],129:[2,30],132:[2,30],133:[2,30],134:[2,30],135:[2,30],136:[2,30],137:[2,30]},{1:[2,31],6:[2,31],25:[2,31],26:[2,31],49:[2,31],54:[2,31],57:[2,31],66:[2,31],67:[2,31],68:[2,31],69:[2,31],71:[2,31],73:[2,31],74:[2,31],78:[2,31],84:[2,31],85:[2,31],86:[2,31],91:[2,31],93:[2,31],102:[2,31],104:[2,31],105:[2,31],106:[2,31],110:[2,31],118:[2,31],126:[2,31],128:[2,31],129:[2,31],132:[2,31],133:[2,31],134:[2,31],135:[2,31],136:[2,31],137:[2,31]},{1:[2,32],6:[2,32],25:[2,32],26:[2,32],49:[2,32],54:[2,32],57:[2,32],66:[2,32],67:[2,32],68:[2,32],69:[2,32],71:[2,32],73:[2,32],74:[2,32],78:[2,32],84:[2,32],85:[2,32],86:[2,32],91:[2,32],93:[2,32],102:[2,32],104:[2,32],105:[2,32],106:[2,32],110:[2,32],118:[2,32],126:[2,32],128:[2,32],129:[2,32],132:[2,32],133:[2,32],134:[2,32],135:[2,32],136:[2,32],137:[2,32]},{1:[2,33],6:[2,33],25:[2,33],26:[2,33],49:[2,33],54:[2,33],57:[2,33],66:[2,33],67:[2,33],68:[2,33],69:[2,33],71:[2,33],73:[2,33],74:[2,33],78:[2,33],84:[2,33],85:[2,33],86:[2,33],91:[2,33],93:[2,33],102:[2,33],104:[2,33],105:[2,33],106:[2,33],110:[2,33],118:[2,33],126:[2,33],128:[2,33],129:[2,33],132:[2,33],133:[2,33],134:[2,33],135:[2,33],136:[2,33],137:[2,33]},{1:[2,34],6:[2,34],25:[2,34],26:[2,34],49:[2,34],54:[2,34],57:[2,34],66:[2,34],67:[2,34],68:[2,34],69:[2,34],71:[2,34],73:[2,34],74:[2,34],78:[2,34],84:[2,34],85:[2,34],86:[2,34],91:[2,34],93:[2,34],102:[2,34],104:[2,34],105:[2,34],106:[2,34],110:[2,34],118:[2,34],126:[2,34],128:[2,34],129:[2,34],132:[2,34],133:[2,34],134:[2,34],135:[2,34],136:[2,34],137:[2,34]},{4:137,5:3,7:4,8:5,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,138],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:139,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,143],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],87:141,88:[1,56],89:[1,57],90:[1,55],91:[1,140],94:142,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,111],6:[2,111],25:[2,111],26:[2,111],49:[2,111],54:[2,111],57:[2,111],66:[2,111],67:[2,111],68:[2,111],69:[2,111],71:[2,111],73:[2,111],74:[2,111],78:[2,111],84:[2,111],85:[2,111],86:[2,111],91:[2,111],93:[2,111],102:[2,111],104:[2,111],105:[2,111],106:[2,111],110:[2,111],118:[2,111],126:[2,111],128:[2,111],129:[2,111],132:[2,111],133:[2,111],134:[2,111],135:[2,111],136:[2,111],137:[2,111]},{1:[2,112],6:[2,112],25:[2,112],26:[2,112],27:145,28:[1,71],49:[2,112],54:[2,112],57:[2,112],66:[2,112],67:[2,112],68:[2,112],69:[2,112],71:[2,112],73:[2,112],74:[2,112],78:[2,112],84:[2,112],85:[2,112],86:[2,112],91:[2,112],93:[2,112],102:[2,112],104:[2,112],105:[2,112],106:[2,112],110:[2,112],118:[2,112],126:[2,112],128:[2,112],129:[2,112],132:[2,112],133:[2,112],134:[2,112],135:[2,112],136:[2,112],137:[2,112]},{25:[2,50]},{25:[2,51]},{1:[2,67],6:[2,67],25:[2,67],26:[2,67],40:[2,67],49:[2,67],54:[2,67],57:[2,67],66:[2,67],67:[2,67],68:[2,67],69:[2,67],71:[2,67],73:[2,67],74:[2,67],78:[2,67],80:[2,67],84:[2,67],85:[2,67],86:[2,67],91:[2,67],93:[2,67],102:[2,67],104:[2,67],105:[2,67],106:[2,67],110:[2,67],118:[2,67],126:[2,67],128:[2,67],129:[2,67],130:[2,67],131:[2,67],132:[2,67],133:[2,67],134:[2,67],135:[2,67],136:[2,67],137:[2,67],138:[2,67]},{1:[2,70],6:[2,70],25:[2,70],26:[2,70],40:[2,70],49:[2,70],54:[2,70],57:[2,70],66:[2,70],67:[2,70],68:[2,70],69:[2,70],71:[2,70],73:[2,70],74:[2,70],78:[2,70],80:[2,70],84:[2,70],85:[2,70],86:[2,70],91:[2,70],93:[2,70],102:[2,70],104:[2,70],105:[2,70],106:[2,70],110:[2,70],118:[2,70],126:[2,70],128:[2,70],129:[2,70],130:[2,70],131:[2,70],132:[2,70],133:[2,70],134:[2,70],135:[2,70],136:[2,70],137:[2,70],138:[2,70]},{7:146,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:147,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:148,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:150,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,24:149,25:[1,112],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{27:155,28:[1,71],44:156,58:157,59:158,64:151,76:[1,68],89:[1,109],90:[1,55],113:152,114:[1,153],115:154},{112:159,116:[1,160],117:[1,161]},{6:[2,90],10:165,25:[2,90],27:166,28:[1,71],29:167,30:[1,69],31:[1,70],41:163,42:164,44:168,46:[1,44],54:[2,90],77:162,78:[2,90],89:[1,109]},{1:[2,26],6:[2,26],25:[2,26],26:[2,26],43:[2,26],49:[2,26],54:[2,26],57:[2,26],66:[2,26],67:[2,26],68:[2,26],69:[2,26],71:[2,26],73:[2,26],74:[2,26],78:[2,26],84:[2,26],85:[2,26],86:[2,26],91:[2,26],93:[2,26],102:[2,26],104:[2,26],105:[2,26],106:[2,26],110:[2,26],118:[2,26],126:[2,26],128:[2,26],129:[2,26],132:[2,26],133:[2,26],134:[2,26],135:[2,26],136:[2,26],137:[2,26]},{1:[2,27],6:[2,27],25:[2,27],26:[2,27],43:[2,27],49:[2,27],54:[2,27],57:[2,27],66:[2,27],67:[2,27],68:[2,27],69:[2,27],71:[2,27],73:[2,27],74:[2,27],78:[2,27],84:[2,27],85:[2,27],86:[2,27],91:[2,27],93:[2,27],102:[2,27],104:[2,27],105:[2,27],106:[2,27],110:[2,27],118:[2,27],126:[2,27],128:[2,27],129:[2,27],132:[2,27],133:[2,27],134:[2,27],135:[2,27],136:[2,27],137:[2,27]},{1:[2,25],6:[2,25],25:[2,25],26:[2,25],40:[2,25],43:[2,25],49:[2,25],54:[2,25],57:[2,25],66:[2,25],67:[2,25],68:[2,25],69:[2,25],71:[2,25],73:[2,25],74:[2,25],78:[2,25],80:[2,25],84:[2,25],85:[2,25],86:[2,25],91:[2,25],93:[2,25],102:[2,25],104:[2,25],105:[2,25],106:[2,25],110:[2,25],116:[2,25],117:[2,25],118:[2,25],126:[2,25],128:[2,25],129:[2,25],130:[2,25],131:[2,25],132:[2,25],133:[2,25],134:[2,25],135:[2,25],136:[2,25],137:[2,25],138:[2,25]},{1:[2,5],5:169,6:[2,5],7:4,8:5,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,26:[2,5],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],102:[2,5],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,193],6:[2,193],25:[2,193],26:[2,193],49:[2,193],54:[2,193],57:[2,193],73:[2,193],78:[2,193],86:[2,193],91:[2,193],93:[2,193],102:[2,193],104:[2,193],105:[2,193],106:[2,193],110:[2,193],118:[2,193],126:[2,193],128:[2,193],129:[2,193],132:[2,193],133:[2,193],134:[2,193],135:[2,193],136:[2,193],137:[2,193]},{7:170,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:171,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:172,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:173,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:174,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:175,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:176,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:177,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,148],6:[2,148],25:[2,148],26:[2,148],49:[2,148],54:[2,148],57:[2,148],73:[2,148],78:[2,148],86:[2,148],91:[2,148],93:[2,148],102:[2,148],104:[2,148],105:[2,148],106:[2,148],110:[2,148],118:[2,148],126:[2,148],128:[2,148],129:[2,148],132:[2,148],133:[2,148],134:[2,148],135:[2,148],136:[2,148],137:[2,148]},{1:[2,153],6:[2,153],25:[2,153],26:[2,153],49:[2,153],54:[2,153],57:[2,153],73:[2,153],78:[2,153],86:[2,153],91:[2,153],93:[2,153],102:[2,153],104:[2,153],105:[2,153],106:[2,153],110:[2,153],118:[2,153],126:[2,153],128:[2,153],129:[2,153],132:[2,153],133:[2,153],134:[2,153],135:[2,153],136:[2,153],137:[2,153]},{7:178,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,147],6:[2,147],25:[2,147],26:[2,147],49:[2,147],54:[2,147],57:[2,147],73:[2,147],78:[2,147],86:[2,147],91:[2,147],93:[2,147],102:[2,147],104:[2,147],105:[2,147],106:[2,147],110:[2,147],118:[2,147],126:[2,147],128:[2,147],129:[2,147],132:[2,147],133:[2,147],134:[2,147],135:[2,147],136:[2,147],137:[2,147]},{1:[2,152],6:[2,152],25:[2,152],26:[2,152],49:[2,152],54:[2,152],57:[2,152],73:[2,152],78:[2,152],86:[2,152],91:[2,152],93:[2,152],102:[2,152],104:[2,152],105:[2,152],106:[2,152],110:[2,152],118:[2,152],126:[2,152],128:[2,152],129:[2,152],132:[2,152],133:[2,152],134:[2,152],135:[2,152],136:[2,152],137:[2,152]},{82:179,85:[1,101]},{1:[2,68],6:[2,68],25:[2,68],26:[2,68],40:[2,68],49:[2,68],54:[2,68],57:[2,68],66:[2,68],67:[2,68],68:[2,68],69:[2,68],71:[2,68],73:[2,68],74:[2,68],78:[2,68],80:[2,68],84:[2,68],85:[2,68],86:[2,68],91:[2,68],93:[2,68],102:[2,68],104:[2,68],105:[2,68],106:[2,68],110:[2,68],118:[2,68],126:[2,68],128:[2,68],129:[2,68],130:[2,68],131:[2,68],132:[2,68],133:[2,68],134:[2,68],135:[2,68],136:[2,68],137:[2,68],138:[2,68]},{85:[2,108]},{27:180,28:[1,71]},{27:181,28:[1,71]},{1:[2,83],6:[2,83],25:[2,83],26:[2,83],27:182,28:[1,71],40:[2,83],49:[2,83],54:[2,83],57:[2,83],66:[2,83],67:[2,83],68:[2,83],69:[2,83],71:[2,83],73:[2,83],74:[2,83],78:[2,83],80:[2,83],84:[2,83],85:[2,83],86:[2,83],91:[2,83],93:[2,83],102:[2,83],104:[2,83],105:[2,83],106:[2,83],110:[2,83],118:[2,83],126:[2,83],128:[2,83],129:[2,83],130:[2,83],131:[2,83],132:[2,83],133:[2,83],134:[2,83],135:[2,83],136:[2,83],137:[2,83],138:[2,83]},{27:183,28:[1,71]},{1:[2,84],6:[2,84],25:[2,84],26:[2,84],40:[2,84],49:[2,84],54:[2,84],57:[2,84],66:[2,84],67:[2,84],68:[2,84],69:[2,84],71:[2,84],73:[2,84],74:[2,84],78:[2,84],80:[2,84],84:[2,84],85:[2,84],86:[2,84],91:[2,84],93:[2,84],102:[2,84],104:[2,84],105:[2,84],106:[2,84],110:[2,84],118:[2,84],126:[2,84],128:[2,84],129:[2,84],130:[2,84],131:[2,84],132:[2,84],133:[2,84],134:[2,84],135:[2,84],136:[2,84],137:[2,84],138:[2,84]},{7:185,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],57:[1,189],58:45,59:46,61:34,63:23,64:24,65:25,72:184,75:186,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],92:187,93:[1,188],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{70:190,71:[1,95],74:[1,96]},{82:191,85:[1,101]},{1:[2,69],6:[2,69],25:[2,69],26:[2,69],40:[2,69],49:[2,69],54:[2,69],57:[2,69],66:[2,69],67:[2,69],68:[2,69],69:[2,69],71:[2,69],73:[2,69],74:[2,69],78:[2,69],80:[2,69],84:[2,69],85:[2,69],86:[2,69],91:[2,69],93:[2,69],102:[2,69],104:[2,69],105:[2,69],106:[2,69],110:[2,69],118:[2,69],126:[2,69],128:[2,69],129:[2,69],130:[2,69],131:[2,69],132:[2,69],133:[2,69],134:[2,69],135:[2,69],136:[2,69],137:[2,69],138:[2,69]},{6:[1,193],7:192,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,194],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,106],6:[2,106],25:[2,106],26:[2,106],49:[2,106],54:[2,106],57:[2,106],66:[2,106],67:[2,106],68:[2,106],69:[2,106],71:[2,106],73:[2,106],74:[2,106],78:[2,106],84:[2,106],85:[2,106],86:[2,106],91:[2,106],93:[2,106],102:[2,106],104:[2,106],105:[2,106],106:[2,106],110:[2,106],118:[2,106],126:[2,106],128:[2,106],129:[2,106],132:[2,106],133:[2,106],134:[2,106],135:[2,106],136:[2,106],137:[2,106]},{7:197,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,143],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],86:[1,195],87:196,88:[1,56],89:[1,57],90:[1,55],94:142,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,52],25:[2,52],49:[1,198],53:200,54:[1,199]},{6:[2,55],25:[2,55],26:[2,55],49:[2,55],54:[2,55]},{6:[2,59],25:[2,59],26:[2,59],40:[1,202],49:[2,59],54:[2,59],57:[1,201]},{6:[2,62],25:[2,62],26:[2,62],40:[2,62],49:[2,62],54:[2,62],57:[2,62]},{6:[2,63],25:[2,63],26:[2,63],40:[2,63],49:[2,63],54:[2,63],57:[2,63]},{6:[2,64],25:[2,64],26:[2,64],40:[2,64],49:[2,64],54:[2,64],57:[2,64]},{6:[2,65],25:[2,65],26:[2,65],40:[2,65],49:[2,65],54:[2,65],57:[2,65]},{27:145,28:[1,71]},{7:197,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,143],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],87:141,88:[1,56],89:[1,57],90:[1,55],91:[1,140],94:142,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,49],6:[2,49],25:[2,49],26:[2,49],49:[2,49],54:[2,49],57:[2,49],73:[2,49],78:[2,49],86:[2,49],91:[2,49],93:[2,49],102:[2,49],104:[2,49],105:[2,49],106:[2,49],110:[2,49],118:[2,49],126:[2,49],128:[2,49],129:[2,49],132:[2,49],133:[2,49],134:[2,49],135:[2,49],136:[2,49],137:[2,49]},{4:204,5:3,7:4,8:5,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,26:[1,203],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,186],6:[2,186],25:[2,186],26:[2,186],49:[2,186],54:[2,186],57:[2,186],73:[2,186],78:[2,186],86:[2,186],91:[2,186],93:[2,186],102:[2,186],103:82,104:[2,186],105:[2,186],106:[2,186],109:83,110:[2,186],111:67,118:[2,186],126:[2,186],128:[2,186],129:[2,186],132:[1,73],133:[2,186],134:[2,186],135:[2,186],136:[2,186],137:[2,186]},{103:85,104:[1,63],106:[1,64],109:86,110:[1,66],111:67,126:[1,84]},{1:[2,187],6:[2,187],25:[2,187],26:[2,187],49:[2,187],54:[2,187],57:[2,187],73:[2,187],78:[2,187],86:[2,187],91:[2,187],93:[2,187],102:[2,187],103:82,104:[2,187],105:[2,187],106:[2,187],109:83,110:[2,187],111:67,118:[2,187],126:[2,187],128:[2,187],129:[2,187],132:[1,73],133:[2,187],134:[2,187],135:[2,187],136:[2,187],137:[2,187]},{1:[2,188],6:[2,188],25:[2,188],26:[2,188],49:[2,188],54:[2,188],57:[2,188],73:[2,188],78:[2,188],86:[2,188],91:[2,188],93:[2,188],102:[2,188],103:82,104:[2,188],105:[2,188],106:[2,188],109:83,110:[2,188],111:67,118:[2,188],126:[2,188],128:[2,188],129:[2,188],132:[1,73],133:[2,188],134:[2,188],135:[2,188],136:[2,188],137:[2,188]},{1:[2,189],6:[2,189],25:[2,189],26:[2,189],49:[2,189],54:[2,189],57:[2,189],66:[2,71],67:[2,71],68:[2,71],69:[2,71],71:[2,71],73:[2,189],74:[2,71],78:[2,189],84:[2,71],85:[2,71],86:[2,189],91:[2,189],93:[2,189],102:[2,189],104:[2,189],105:[2,189],106:[2,189],110:[2,189],118:[2,189],126:[2,189],128:[2,189],129:[2,189],132:[2,189],133:[2,189],134:[2,189],135:[2,189],136:[2,189],137:[2,189]},{62:88,66:[1,90],67:[1,91],68:[1,92],69:[1,93],70:94,71:[1,95],74:[1,96],81:87,84:[1,89],85:[2,107]},{62:98,66:[1,90],67:[1,91],68:[1,92],69:[1,93],70:94,71:[1,95],74:[1,96],81:97,84:[1,89],85:[2,107]},{66:[2,74],67:[2,74],68:[2,74],69:[2,74],71:[2,74],74:[2,74],84:[2,74],85:[2,74]},{1:[2,190],6:[2,190],25:[2,190],26:[2,190],49:[2,190],54:[2,190],57:[2,190],66:[2,71],67:[2,71],68:[2,71],69:[2,71],71:[2,71],73:[2,190],74:[2,71],78:[2,190],84:[2,71],85:[2,71],86:[2,190],91:[2,190],93:[2,190],102:[2,190],104:[2,190],105:[2,190],106:[2,190],110:[2,190],118:[2,190],126:[2,190],128:[2,190],129:[2,190],132:[2,190],133:[2,190],134:[2,190],135:[2,190],136:[2,190],137:[2,190]},{1:[2,191],6:[2,191],25:[2,191],26:[2,191],49:[2,191],54:[2,191],57:[2,191],73:[2,191],78:[2,191],86:[2,191],91:[2,191],93:[2,191],102:[2,191],104:[2,191],105:[2,191],106:[2,191],110:[2,191],118:[2,191],126:[2,191],128:[2,191],129:[2,191],132:[2,191],133:[2,191],134:[2,191],135:[2,191],136:[2,191],137:[2,191]},{1:[2,192],6:[2,192],25:[2,192],26:[2,192],49:[2,192],54:[2,192],57:[2,192],73:[2,192],78:[2,192],86:[2,192],91:[2,192],93:[2,192],102:[2,192],104:[2,192],105:[2,192],106:[2,192],110:[2,192],118:[2,192],126:[2,192],128:[2,192],129:[2,192],132:[2,192],133:[2,192],134:[2,192],135:[2,192],136:[2,192],137:[2,192]},{6:[1,207],7:205,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,206],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:208,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{24:209,25:[1,112],125:[1,210]},{1:[2,132],6:[2,132],25:[2,132],26:[2,132],49:[2,132],54:[2,132],57:[2,132],73:[2,132],78:[2,132],86:[2,132],91:[2,132],93:[2,132],97:211,98:[1,212],99:[1,213],102:[2,132],104:[2,132],105:[2,132],106:[2,132],110:[2,132],118:[2,132],126:[2,132],128:[2,132],129:[2,132],132:[2,132],133:[2,132],134:[2,132],135:[2,132],136:[2,132],137:[2,132]},{1:[2,146],6:[2,146],25:[2,146],26:[2,146],49:[2,146],54:[2,146],57:[2,146],73:[2,146],78:[2,146],86:[2,146],91:[2,146],93:[2,146],102:[2,146],104:[2,146],105:[2,146],106:[2,146],110:[2,146],118:[2,146],126:[2,146],128:[2,146],129:[2,146],132:[2,146],133:[2,146],134:[2,146],135:[2,146],136:[2,146],137:[2,146]},{1:[2,154],6:[2,154],25:[2,154],26:[2,154],49:[2,154],54:[2,154],57:[2,154],73:[2,154],78:[2,154],86:[2,154],91:[2,154],93:[2,154],102:[2,154],104:[2,154],105:[2,154],106:[2,154],110:[2,154],118:[2,154],126:[2,154],128:[2,154],129:[2,154],132:[2,154],133:[2,154],134:[2,154],135:[2,154],136:[2,154],137:[2,154]},{25:[1,214],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{120:215,122:216,123:[1,217]},{1:[2,96],6:[2,96],25:[2,96],26:[2,96],49:[2,96],54:[2,96],57:[2,96],73:[2,96],78:[2,96],86:[2,96],91:[2,96],93:[2,96],102:[2,96],104:[2,96],105:[2,96],106:[2,96],110:[2,96],118:[2,96],126:[2,96],128:[2,96],129:[2,96],132:[2,96],133:[2,96],134:[2,96],135:[2,96],136:[2,96],137:[2,96]},{7:218,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,99],6:[2,99],24:219,25:[1,112],26:[2,99],49:[2,99],54:[2,99],57:[2,99],66:[2,71],67:[2,71],68:[2,71],69:[2,71],71:[2,71],73:[2,99],74:[2,71],78:[2,99],80:[1,220],84:[2,71],85:[2,71],86:[2,99],91:[2,99],93:[2,99],102:[2,99],104:[2,99],105:[2,99],106:[2,99],110:[2,99],118:[2,99],126:[2,99],128:[2,99],129:[2,99],132:[2,99],133:[2,99],134:[2,99],135:[2,99],136:[2,99],137:[2,99]},{1:[2,139],6:[2,139],25:[2,139],26:[2,139],49:[2,139],54:[2,139],57:[2,139],73:[2,139],78:[2,139],86:[2,139],91:[2,139],93:[2,139],102:[2,139],103:82,104:[2,139],105:[2,139],106:[2,139],109:83,110:[2,139],111:67,118:[2,139],126:[2,139],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,45],6:[2,45],26:[2,45],102:[2,45],103:82,104:[2,45],106:[2,45],109:83,110:[2,45],111:67,126:[2,45],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[1,72],102:[1,221]},{4:222,5:3,7:4,8:5,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,128],25:[2,128],54:[2,128],57:[1,224],91:[2,128],92:223,93:[1,188],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,114],6:[2,114],25:[2,114],26:[2,114],40:[2,114],49:[2,114],54:[2,114],57:[2,114],66:[2,114],67:[2,114],68:[2,114],69:[2,114],71:[2,114],73:[2,114],74:[2,114],78:[2,114],84:[2,114],85:[2,114],86:[2,114],91:[2,114],93:[2,114],102:[2,114],104:[2,114],105:[2,114],106:[2,114],110:[2,114],116:[2,114],117:[2,114],118:[2,114],126:[2,114],128:[2,114],129:[2,114],132:[2,114],133:[2,114],134:[2,114],135:[2,114],136:[2,114],137:[2,114]},{6:[2,52],25:[2,52],53:225,54:[1,226],91:[2,52]},{6:[2,123],25:[2,123],26:[2,123],54:[2,123],86:[2,123],91:[2,123]},{7:197,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,143],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],87:227,88:[1,56],89:[1,57],90:[1,55],94:142,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,129],25:[2,129],26:[2,129],54:[2,129],86:[2,129],91:[2,129]},{1:[2,113],6:[2,113],25:[2,113],26:[2,113],40:[2,113],43:[2,113],49:[2,113],54:[2,113],57:[2,113],66:[2,113],67:[2,113],68:[2,113],69:[2,113],71:[2,113],73:[2,113],74:[2,113],78:[2,113],80:[2,113],84:[2,113],85:[2,113],86:[2,113],91:[2,113],93:[2,113],102:[2,113],104:[2,113],105:[2,113],106:[2,113],110:[2,113],116:[2,113],117:[2,113],118:[2,113],126:[2,113],128:[2,113],129:[2,113],130:[2,113],131:[2,113],132:[2,113],133:[2,113],134:[2,113],135:[2,113],136:[2,113],137:[2,113],138:[2,113]},{24:228,25:[1,112],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,142],6:[2,142],25:[2,142],26:[2,142],49:[2,142],54:[2,142],57:[2,142],73:[2,142],78:[2,142],86:[2,142],91:[2,142],93:[2,142],102:[2,142],103:82,104:[1,63],105:[1,229],106:[1,64],109:83,110:[1,66],111:67,118:[2,142],126:[2,142],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,144],6:[2,144],25:[2,144],26:[2,144],49:[2,144],54:[2,144],57:[2,144],73:[2,144],78:[2,144],86:[2,144],91:[2,144],93:[2,144],102:[2,144],103:82,104:[1,63],105:[1,230],106:[1,64],109:83,110:[1,66],111:67,118:[2,144],126:[2,144],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,150],6:[2,150],25:[2,150],26:[2,150],49:[2,150],54:[2,150],57:[2,150],73:[2,150],78:[2,150],86:[2,150],91:[2,150],93:[2,150],102:[2,150],104:[2,150],105:[2,150],106:[2,150],110:[2,150],118:[2,150],126:[2,150],128:[2,150],129:[2,150],132:[2,150],133:[2,150],134:[2,150],135:[2,150],136:[2,150],137:[2,150]},{1:[2,151],6:[2,151],25:[2,151],26:[2,151],49:[2,151],54:[2,151],57:[2,151],73:[2,151],78:[2,151],86:[2,151],91:[2,151],93:[2,151],102:[2,151],103:82,104:[1,63],105:[2,151],106:[1,64],109:83,110:[1,66],111:67,118:[2,151],126:[2,151],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,155],6:[2,155],25:[2,155],26:[2,155],49:[2,155],54:[2,155],57:[2,155],73:[2,155],78:[2,155],86:[2,155],91:[2,155],93:[2,155],102:[2,155],104:[2,155],105:[2,155],106:[2,155],110:[2,155],118:[2,155],126:[2,155],128:[2,155],129:[2,155],132:[2,155],133:[2,155],134:[2,155],135:[2,155],136:[2,155],137:[2,155]},{116:[2,157],117:[2,157]},{27:155,28:[1,71],44:156,58:157,59:158,76:[1,68],89:[1,109],90:[1,110],113:231,115:154},{54:[1,232],116:[2,163],117:[2,163]},{54:[2,159],116:[2,159],117:[2,159]},{54:[2,160],116:[2,160],117:[2,160]},{54:[2,161],116:[2,161],117:[2,161]},{54:[2,162],116:[2,162],117:[2,162]},{1:[2,156],6:[2,156],25:[2,156],26:[2,156],49:[2,156],54:[2,156],57:[2,156],73:[2,156],78:[2,156],86:[2,156],91:[2,156],93:[2,156],102:[2,156],104:[2,156],105:[2,156],106:[2,156],110:[2,156],118:[2,156],126:[2,156],128:[2,156],129:[2,156],132:[2,156],133:[2,156],134:[2,156],135:[2,156],136:[2,156],137:[2,156]},{7:233,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:234,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,52],25:[2,52],53:235,54:[1,236],78:[2,52]},{6:[2,91],25:[2,91],26:[2,91],54:[2,91],78:[2,91]},{6:[2,38],25:[2,38],26:[2,38],43:[1,237],54:[2,38],78:[2,38]},{6:[2,41],25:[2,41],26:[2,41],54:[2,41],78:[2,41]},{6:[2,42],25:[2,42],26:[2,42],43:[2,42],54:[2,42],78:[2,42]},{6:[2,43],25:[2,43],26:[2,43],43:[2,43],54:[2,43],78:[2,43]},{6:[2,44],25:[2,44],26:[2,44],43:[2,44],54:[2,44],78:[2,44]},{1:[2,4],6:[2,4],26:[2,4],102:[2,4]},{1:[2,194],6:[2,194],25:[2,194],26:[2,194],49:[2,194],54:[2,194],57:[2,194],73:[2,194],78:[2,194],86:[2,194],91:[2,194],93:[2,194],102:[2,194],103:82,104:[2,194],105:[2,194],106:[2,194],109:83,110:[2,194],111:67,118:[2,194],126:[2,194],128:[2,194],129:[2,194],132:[1,73],133:[1,76],134:[2,194],135:[2,194],136:[2,194],137:[2,194]},{1:[2,195],6:[2,195],25:[2,195],26:[2,195],49:[2,195],54:[2,195],57:[2,195],73:[2,195],78:[2,195],86:[2,195],91:[2,195],93:[2,195],102:[2,195],103:82,104:[2,195],105:[2,195],106:[2,195],109:83,110:[2,195],111:67,118:[2,195],126:[2,195],128:[2,195],129:[2,195],132:[1,73],133:[1,76],134:[2,195],135:[2,195],136:[2,195],137:[2,195]},{1:[2,196],6:[2,196],25:[2,196],26:[2,196],49:[2,196],54:[2,196],57:[2,196],73:[2,196],78:[2,196],86:[2,196],91:[2,196],93:[2,196],102:[2,196],103:82,104:[2,196],105:[2,196],106:[2,196],109:83,110:[2,196],111:67,118:[2,196],126:[2,196],128:[2,196],129:[2,196],132:[1,73],133:[2,196],134:[2,196],135:[2,196],136:[2,196],137:[2,196]},{1:[2,197],6:[2,197],25:[2,197],26:[2,197],49:[2,197],54:[2,197],57:[2,197],73:[2,197],78:[2,197],86:[2,197],91:[2,197],93:[2,197],102:[2,197],103:82,104:[2,197],105:[2,197],106:[2,197],109:83,110:[2,197],111:67,118:[2,197],126:[2,197],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[2,197],135:[2,197],136:[2,197],137:[2,197]},{1:[2,198],6:[2,198],25:[2,198],26:[2,198],49:[2,198],54:[2,198],57:[2,198],73:[2,198],78:[2,198],86:[2,198],91:[2,198],93:[2,198],102:[2,198],103:82,104:[2,198],105:[2,198],106:[2,198],109:83,110:[2,198],111:67,118:[2,198],126:[2,198],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[2,198],136:[2,198],137:[1,80]},{1:[2,199],6:[2,199],25:[2,199],26:[2,199],49:[2,199],54:[2,199],57:[2,199],73:[2,199],78:[2,199],86:[2,199],91:[2,199],93:[2,199],102:[2,199],103:82,104:[2,199],105:[2,199],106:[2,199],109:83,110:[2,199],111:67,118:[2,199],126:[2,199],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[2,199],137:[1,80]},{1:[2,200],6:[2,200],25:[2,200],26:[2,200],49:[2,200],54:[2,200],57:[2,200],73:[2,200],78:[2,200],86:[2,200],91:[2,200],93:[2,200],102:[2,200],103:82,104:[2,200],105:[2,200],106:[2,200],109:83,110:[2,200],111:67,118:[2,200],126:[2,200],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[2,200],136:[2,200],137:[2,200]},{1:[2,185],6:[2,185],25:[2,185],26:[2,185],49:[2,185],54:[2,185],57:[2,185],73:[2,185],78:[2,185],86:[2,185],91:[2,185],93:[2,185],102:[2,185],103:82,104:[1,63],105:[2,185],106:[1,64],109:83,110:[1,66],111:67,118:[2,185],126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,184],6:[2,184],25:[2,184],26:[2,184],49:[2,184],54:[2,184],57:[2,184],73:[2,184],78:[2,184],86:[2,184],91:[2,184],93:[2,184],102:[2,184],103:82,104:[1,63],105:[2,184],106:[1,64],109:83,110:[1,66],111:67,118:[2,184],126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,103],6:[2,103],25:[2,103],26:[2,103],49:[2,103],54:[2,103],57:[2,103],66:[2,103],67:[2,103],68:[2,103],69:[2,103],71:[2,103],73:[2,103],74:[2,103],78:[2,103],84:[2,103],85:[2,103],86:[2,103],91:[2,103],93:[2,103],102:[2,103],104:[2,103],105:[2,103],106:[2,103],110:[2,103],118:[2,103],126:[2,103],128:[2,103],129:[2,103],132:[2,103],133:[2,103],134:[2,103],135:[2,103],136:[2,103],137:[2,103]},{1:[2,79],6:[2,79],25:[2,79],26:[2,79],40:[2,79],49:[2,79],54:[2,79],57:[2,79],66:[2,79],67:[2,79],68:[2,79],69:[2,79],71:[2,79],73:[2,79],74:[2,79],78:[2,79],80:[2,79],84:[2,79],85:[2,79],86:[2,79],91:[2,79],93:[2,79],102:[2,79],104:[2,79],105:[2,79],106:[2,79],110:[2,79],118:[2,79],126:[2,79],128:[2,79],129:[2,79],130:[2,79],131:[2,79],132:[2,79],133:[2,79],134:[2,79],135:[2,79],136:[2,79],137:[2,79],138:[2,79]},{1:[2,80],6:[2,80],25:[2,80],26:[2,80],40:[2,80],49:[2,80],54:[2,80],57:[2,80],66:[2,80],67:[2,80],68:[2,80],69:[2,80],71:[2,80],73:[2,80],74:[2,80],78:[2,80],80:[2,80],84:[2,80],85:[2,80],86:[2,80],91:[2,80],93:[2,80],102:[2,80],104:[2,80],105:[2,80],106:[2,80],110:[2,80],118:[2,80],126:[2,80],128:[2,80],129:[2,80],130:[2,80],131:[2,80],132:[2,80],133:[2,80],134:[2,80],135:[2,80],136:[2,80],137:[2,80],138:[2,80]},{1:[2,81],6:[2,81],25:[2,81],26:[2,81],40:[2,81],49:[2,81],54:[2,81],57:[2,81],66:[2,81],67:[2,81],68:[2,81],69:[2,81],71:[2,81],73:[2,81],74:[2,81],78:[2,81],80:[2,81],84:[2,81],85:[2,81],86:[2,81],91:[2,81],93:[2,81],102:[2,81],104:[2,81],105:[2,81],106:[2,81],110:[2,81],118:[2,81],126:[2,81],128:[2,81],129:[2,81],130:[2,81],131:[2,81],132:[2,81],133:[2,81],134:[2,81],135:[2,81],136:[2,81],137:[2,81],138:[2,81]},{1:[2,82],6:[2,82],25:[2,82],26:[2,82],40:[2,82],49:[2,82],54:[2,82],57:[2,82],66:[2,82],67:[2,82],68:[2,82],69:[2,82],71:[2,82],73:[2,82],74:[2,82],78:[2,82],80:[2,82],84:[2,82],85:[2,82],86:[2,82],91:[2,82],93:[2,82],102:[2,82],104:[2,82],105:[2,82],106:[2,82],110:[2,82],118:[2,82],126:[2,82],128:[2,82],129:[2,82],130:[2,82],131:[2,82],132:[2,82],133:[2,82],134:[2,82],135:[2,82],136:[2,82],137:[2,82],138:[2,82]},{73:[1,238]},{57:[1,189],73:[2,87],92:239,93:[1,188],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{73:[2,88]},{7:240,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,73:[2,122],76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{11:[2,116],28:[2,116],30:[2,116],31:[2,116],33:[2,116],34:[2,116],35:[2,116],36:[2,116],37:[2,116],38:[2,116],45:[2,116],46:[2,116],47:[2,116],51:[2,116],52:[2,116],73:[2,116],76:[2,116],79:[2,116],83:[2,116],88:[2,116],89:[2,116],90:[2,116],96:[2,116],100:[2,116],101:[2,116],104:[2,116],106:[2,116],108:[2,116],110:[2,116],119:[2,116],125:[2,116],127:[2,116],128:[2,116],129:[2,116],130:[2,116],131:[2,116]},{11:[2,117],28:[2,117],30:[2,117],31:[2,117],33:[2,117],34:[2,117],35:[2,117],36:[2,117],37:[2,117],38:[2,117],45:[2,117],46:[2,117],47:[2,117],51:[2,117],52:[2,117],73:[2,117],76:[2,117],79:[2,117],83:[2,117],88:[2,117],89:[2,117],90:[2,117],96:[2,117],100:[2,117],101:[2,117],104:[2,117],106:[2,117],108:[2,117],110:[2,117],119:[2,117],125:[2,117],127:[2,117],128:[2,117],129:[2,117],130:[2,117],131:[2,117]},{1:[2,86],6:[2,86],25:[2,86],26:[2,86],40:[2,86],49:[2,86],54:[2,86],57:[2,86],66:[2,86],67:[2,86],68:[2,86],69:[2,86],71:[2,86],73:[2,86],74:[2,86],78:[2,86],80:[2,86],84:[2,86],85:[2,86],86:[2,86],91:[2,86],93:[2,86],102:[2,86],104:[2,86],105:[2,86],106:[2,86],110:[2,86],118:[2,86],126:[2,86],128:[2,86],129:[2,86],130:[2,86],131:[2,86],132:[2,86],133:[2,86],134:[2,86],135:[2,86],136:[2,86],137:[2,86],138:[2,86]},{1:[2,104],6:[2,104],25:[2,104],26:[2,104],49:[2,104],54:[2,104],57:[2,104],66:[2,104],67:[2,104],68:[2,104],69:[2,104],71:[2,104],73:[2,104],74:[2,104],78:[2,104],84:[2,104],85:[2,104],86:[2,104],91:[2,104],93:[2,104],102:[2,104],104:[2,104],105:[2,104],106:[2,104],110:[2,104],118:[2,104],126:[2,104],128:[2,104],129:[2,104],132:[2,104],133:[2,104],134:[2,104],135:[2,104],136:[2,104],137:[2,104]},{1:[2,35],6:[2,35],25:[2,35],26:[2,35],49:[2,35],54:[2,35],57:[2,35],73:[2,35],78:[2,35],86:[2,35],91:[2,35],93:[2,35],102:[2,35],103:82,104:[2,35],105:[2,35],106:[2,35],109:83,110:[2,35],111:67,118:[2,35],126:[2,35],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{7:241,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:242,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,109],6:[2,109],25:[2,109],26:[2,109],49:[2,109],54:[2,109],57:[2,109],66:[2,109],67:[2,109],68:[2,109],69:[2,109],71:[2,109],73:[2,109],74:[2,109],78:[2,109],84:[2,109],85:[2,109],86:[2,109],91:[2,109],93:[2,109],102:[2,109],104:[2,109],105:[2,109],106:[2,109],110:[2,109],118:[2,109],126:[2,109],128:[2,109],129:[2,109],132:[2,109],133:[2,109],134:[2,109],135:[2,109],136:[2,109],137:[2,109]},{6:[2,52],25:[2,52],53:243,54:[1,226],86:[2,52]},{6:[2,128],25:[2,128],26:[2,128],54:[2,128],57:[1,244],86:[2,128],91:[2,128],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{50:245,51:[1,58],52:[1,59]},{6:[2,53],25:[2,53],26:[2,53],27:105,28:[1,71],44:106,55:246,56:104,58:107,59:108,76:[1,68],89:[1,109],90:[1,110]},{6:[1,247],25:[1,248]},{6:[2,60],25:[2,60],26:[2,60],49:[2,60],54:[2,60]},{7:249,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,23],6:[2,23],25:[2,23],26:[2,23],49:[2,23],54:[2,23],57:[2,23],73:[2,23],78:[2,23],86:[2,23],91:[2,23],93:[2,23],98:[2,23],99:[2,23],102:[2,23],104:[2,23],105:[2,23],106:[2,23],110:[2,23],118:[2,23],121:[2,23],123:[2,23],126:[2,23],128:[2,23],129:[2,23],132:[2,23],133:[2,23],134:[2,23],135:[2,23],136:[2,23],137:[2,23]},{6:[1,72],26:[1,250]},{1:[2,201],6:[2,201],25:[2,201],26:[2,201],49:[2,201],54:[2,201],57:[2,201],73:[2,201],78:[2,201],86:[2,201],91:[2,201],93:[2,201],102:[2,201],103:82,104:[2,201],105:[2,201],106:[2,201],109:83,110:[2,201],111:67,118:[2,201],126:[2,201],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{7:251,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:252,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,204],6:[2,204],25:[2,204],26:[2,204],49:[2,204],54:[2,204],57:[2,204],73:[2,204],78:[2,204],86:[2,204],91:[2,204],93:[2,204],102:[2,204],103:82,104:[2,204],105:[2,204],106:[2,204],109:83,110:[2,204],111:67,118:[2,204],126:[2,204],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,183],6:[2,183],25:[2,183],26:[2,183],49:[2,183],54:[2,183],57:[2,183],73:[2,183],78:[2,183],86:[2,183],91:[2,183],93:[2,183],102:[2,183],104:[2,183],105:[2,183],106:[2,183],110:[2,183],118:[2,183],126:[2,183],128:[2,183],129:[2,183],132:[2,183],133:[2,183],134:[2,183],135:[2,183],136:[2,183],137:[2,183]},{7:253,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,133],6:[2,133],25:[2,133],26:[2,133],49:[2,133],54:[2,133],57:[2,133],73:[2,133],78:[2,133],86:[2,133],91:[2,133],93:[2,133],98:[1,254],102:[2,133],104:[2,133],105:[2,133],106:[2,133],110:[2,133],118:[2,133],126:[2,133],128:[2,133],129:[2,133],132:[2,133],133:[2,133],134:[2,133],135:[2,133],136:[2,133],137:[2,133]},{24:255,25:[1,112]},{24:258,25:[1,112],27:256,28:[1,71],59:257,76:[1,68]},{120:259,122:216,123:[1,217]},{26:[1,260],121:[1,261],122:262,123:[1,217]},{26:[2,176],121:[2,176],123:[2,176]},{7:264,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],95:263,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,97],6:[2,97],24:265,25:[1,112],26:[2,97],49:[2,97],54:[2,97],57:[2,97],73:[2,97],78:[2,97],86:[2,97],91:[2,97],93:[2,97],102:[2,97],103:82,104:[1,63],105:[2,97],106:[1,64],109:83,110:[1,66],111:67,118:[2,97],126:[2,97],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,100],6:[2,100],25:[2,100],26:[2,100],49:[2,100],54:[2,100],57:[2,100],73:[2,100],78:[2,100],86:[2,100],91:[2,100],93:[2,100],102:[2,100],104:[2,100],105:[2,100],106:[2,100],110:[2,100],118:[2,100],126:[2,100],128:[2,100],129:[2,100],132:[2,100],133:[2,100],134:[2,100],135:[2,100],136:[2,100],137:[2,100]},{7:266,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,140],6:[2,140],25:[2,140],26:[2,140],49:[2,140],54:[2,140],57:[2,140],66:[2,140],67:[2,140],68:[2,140],69:[2,140],71:[2,140],73:[2,140],74:[2,140],78:[2,140],84:[2,140],85:[2,140],86:[2,140],91:[2,140],93:[2,140],102:[2,140],104:[2,140],105:[2,140],106:[2,140],110:[2,140],118:[2,140],126:[2,140],128:[2,140],129:[2,140],132:[2,140],133:[2,140],134:[2,140],135:[2,140],136:[2,140],137:[2,140]},{6:[1,72],26:[1,267]},{7:268,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,66],11:[2,117],25:[2,66],28:[2,117],30:[2,117],31:[2,117],33:[2,117],34:[2,117],35:[2,117],36:[2,117],37:[2,117],38:[2,117],45:[2,117],46:[2,117],47:[2,117],51:[2,117],52:[2,117],54:[2,66],76:[2,117],79:[2,117],83:[2,117],88:[2,117],89:[2,117],90:[2,117],91:[2,66],96:[2,117],100:[2,117],101:[2,117],104:[2,117],106:[2,117],108:[2,117],110:[2,117],119:[2,117],125:[2,117],127:[2,117],128:[2,117],129:[2,117],130:[2,117],131:[2,117]},{6:[1,270],25:[1,271],91:[1,269]},{6:[2,53],7:197,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[2,53],26:[2,53],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],86:[2,53],88:[1,56],89:[1,57],90:[1,55],91:[2,53],94:272,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,52],25:[2,52],26:[2,52],53:273,54:[1,226]},{1:[2,180],6:[2,180],25:[2,180],26:[2,180],49:[2,180],54:[2,180],57:[2,180],73:[2,180],78:[2,180],86:[2,180],91:[2,180],93:[2,180],102:[2,180],104:[2,180],105:[2,180],106:[2,180],110:[2,180],118:[2,180],121:[2,180],126:[2,180],128:[2,180],129:[2,180],132:[2,180],133:[2,180],134:[2,180],135:[2,180],136:[2,180],137:[2,180]},{7:274,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:275,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{116:[2,158],117:[2,158]},{27:155,28:[1,71],44:156,58:157,59:158,76:[1,68],89:[1,109],90:[1,110],115:276},{1:[2,165],6:[2,165],25:[2,165],26:[2,165]</string> </value>
        </item>
        <item>
            <key> <string>next</string> </key>
            <value>
              <persistent> <string encoding="base64">AAAAAAAAAAU=</string> </persistent>
            </value>
        </item>
      </dictionary>
    </pickle>
  </record>
  <record id="5" aka="AAAAAAAAAAU=">
    <pickle>
      <global name="Pdata" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

,49:[2,165],54:[2,165],57:[2,165],73:[2,165],78:[2,165],86:[2,165],91:[2,165],93:[2,165],102:[2,165],103:82,104:[2,165],105:[1,277],106:[2,165],109:83,110:[2,165],111:67,118:[1,278],126:[2,165],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,166],6:[2,166],25:[2,166],26:[2,166],49:[2,166],54:[2,166],57:[2,166],73:[2,166],78:[2,166],86:[2,166],91:[2,166],93:[2,166],102:[2,166],103:82,104:[2,166],105:[1,279],106:[2,166],109:83,110:[2,166],111:67,118:[2,166],126:[2,166],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[1,281],25:[1,282],78:[1,280]},{6:[2,53],10:165,25:[2,53],26:[2,53],27:166,28:[1,71],29:167,30:[1,69],31:[1,70],41:283,42:164,44:168,46:[1,44],78:[2,53],89:[1,109]},{7:284,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,285],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,85],6:[2,85],25:[2,85],26:[2,85],40:[2,85],49:[2,85],54:[2,85],57:[2,85],66:[2,85],67:[2,85],68:[2,85],69:[2,85],71:[2,85],73:[2,85],74:[2,85],78:[2,85],80:[2,85],84:[2,85],85:[2,85],86:[2,85],91:[2,85],93:[2,85],102:[2,85],104:[2,85],105:[2,85],106:[2,85],110:[2,85],118:[2,85],126:[2,85],128:[2,85],129:[2,85],130:[2,85],131:[2,85],132:[2,85],133:[2,85],134:[2,85],135:[2,85],136:[2,85],137:[2,85],138:[2,85]},{7:286,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,73:[2,120],76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{73:[2,121],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,36],6:[2,36],25:[2,36],26:[2,36],49:[2,36],54:[2,36],57:[2,36],73:[2,36],78:[2,36],86:[2,36],91:[2,36],93:[2,36],102:[2,36],103:82,104:[2,36],105:[2,36],106:[2,36],109:83,110:[2,36],111:67,118:[2,36],126:[2,36],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{26:[1,287],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[1,270],25:[1,271],86:[1,288]},{6:[2,66],25:[2,66],26:[2,66],54:[2,66],86:[2,66],91:[2,66]},{24:289,25:[1,112]},{6:[2,56],25:[2,56],26:[2,56],49:[2,56],54:[2,56]},{27:105,28:[1,71],44:106,55:290,56:104,58:107,59:108,76:[1,68],89:[1,109],90:[1,110]},{6:[2,54],25:[2,54],26:[2,54],27:105,28:[1,71],44:106,48:291,54:[2,54],55:103,56:104,58:107,59:108,76:[1,68],89:[1,109],90:[1,110]},{6:[2,61],25:[2,61],26:[2,61],49:[2,61],54:[2,61],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,24],6:[2,24],25:[2,24],26:[2,24],49:[2,24],54:[2,24],57:[2,24],73:[2,24],78:[2,24],86:[2,24],91:[2,24],93:[2,24],98:[2,24],99:[2,24],102:[2,24],104:[2,24],105:[2,24],106:[2,24],110:[2,24],118:[2,24],121:[2,24],123:[2,24],126:[2,24],128:[2,24],129:[2,24],132:[2,24],133:[2,24],134:[2,24],135:[2,24],136:[2,24],137:[2,24]},{26:[1,292],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,203],6:[2,203],25:[2,203],26:[2,203],49:[2,203],54:[2,203],57:[2,203],73:[2,203],78:[2,203],86:[2,203],91:[2,203],93:[2,203],102:[2,203],103:82,104:[2,203],105:[2,203],106:[2,203],109:83,110:[2,203],111:67,118:[2,203],126:[2,203],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{24:293,25:[1,112],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{24:294,25:[1,112]},{1:[2,134],6:[2,134],25:[2,134],26:[2,134],49:[2,134],54:[2,134],57:[2,134],73:[2,134],78:[2,134],86:[2,134],91:[2,134],93:[2,134],102:[2,134],104:[2,134],105:[2,134],106:[2,134],110:[2,134],118:[2,134],126:[2,134],128:[2,134],129:[2,134],132:[2,134],133:[2,134],134:[2,134],135:[2,134],136:[2,134],137:[2,134]},{24:295,25:[1,112]},{24:296,25:[1,112]},{1:[2,138],6:[2,138],25:[2,138],26:[2,138],49:[2,138],54:[2,138],57:[2,138],73:[2,138],78:[2,138],86:[2,138],91:[2,138],93:[2,138],98:[2,138],102:[2,138],104:[2,138],105:[2,138],106:[2,138],110:[2,138],118:[2,138],126:[2,138],128:[2,138],129:[2,138],132:[2,138],133:[2,138],134:[2,138],135:[2,138],136:[2,138],137:[2,138]},{26:[1,297],121:[1,298],122:262,123:[1,217]},{1:[2,174],6:[2,174],25:[2,174],26:[2,174],49:[2,174],54:[2,174],57:[2,174],73:[2,174],78:[2,174],86:[2,174],91:[2,174],93:[2,174],102:[2,174],104:[2,174],105:[2,174],106:[2,174],110:[2,174],118:[2,174],126:[2,174],128:[2,174],129:[2,174],132:[2,174],133:[2,174],134:[2,174],135:[2,174],136:[2,174],137:[2,174]},{24:299,25:[1,112]},{26:[2,177],121:[2,177],123:[2,177]},{24:300,25:[1,112],54:[1,301]},{25:[2,130],54:[2,130],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,98],6:[2,98],25:[2,98],26:[2,98],49:[2,98],54:[2,98],57:[2,98],73:[2,98],78:[2,98],86:[2,98],91:[2,98],93:[2,98],102:[2,98],104:[2,98],105:[2,98],106:[2,98],110:[2,98],118:[2,98],126:[2,98],128:[2,98],129:[2,98],132:[2,98],133:[2,98],134:[2,98],135:[2,98],136:[2,98],137:[2,98]},{1:[2,101],6:[2,101],24:302,25:[1,112],26:[2,101],49:[2,101],54:[2,101],57:[2,101],73:[2,101],78:[2,101],86:[2,101],91:[2,101],93:[2,101],102:[2,101],103:82,104:[1,63],105:[2,101],106:[1,64],109:83,110:[1,66],111:67,118:[2,101],126:[2,101],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{102:[1,303]},{91:[1,304],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,115],6:[2,115],25:[2,115],26:[2,115],40:[2,115],49:[2,115],54:[2,115],57:[2,115],66:[2,115],67:[2,115],68:[2,115],69:[2,115],71:[2,115],73:[2,115],74:[2,115],78:[2,115],84:[2,115],85:[2,115],86:[2,115],91:[2,115],93:[2,115],102:[2,115],104:[2,115],105:[2,115],106:[2,115],110:[2,115],116:[2,115],117:[2,115],118:[2,115],126:[2,115],128:[2,115],129:[2,115],132:[2,115],133:[2,115],134:[2,115],135:[2,115],136:[2,115],137:[2,115]},{7:197,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],94:305,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:197,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,25:[1,143],27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,60:144,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],87:306,88:[1,56],89:[1,57],90:[1,55],94:142,96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[2,124],25:[2,124],26:[2,124],54:[2,124],86:[2,124],91:[2,124]},{6:[1,270],25:[1,271],26:[1,307]},{1:[2,143],6:[2,143],25:[2,143],26:[2,143],49:[2,143],54:[2,143],57:[2,143],73:[2,143],78:[2,143],86:[2,143],91:[2,143],93:[2,143],102:[2,143],103:82,104:[1,63],105:[2,143],106:[1,64],109:83,110:[1,66],111:67,118:[2,143],126:[2,143],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,145],6:[2,145],25:[2,145],26:[2,145],49:[2,145],54:[2,145],57:[2,145],73:[2,145],78:[2,145],86:[2,145],91:[2,145],93:[2,145],102:[2,145],103:82,104:[1,63],105:[2,145],106:[1,64],109:83,110:[1,66],111:67,118:[2,145],126:[2,145],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{116:[2,164],117:[2,164]},{7:308,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:309,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:310,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,89],6:[2,89],25:[2,89],26:[2,89],40:[2,89],49:[2,89],54:[2,89],57:[2,89],66:[2,89],67:[2,89],68:[2,89],69:[2,89],71:[2,89],73:[2,89],74:[2,89],78:[2,89],84:[2,89],85:[2,89],86:[2,89],91:[2,89],93:[2,89],102:[2,89],104:[2,89],105:[2,89],106:[2,89],110:[2,89],116:[2,89],117:[2,89],118:[2,89],126:[2,89],128:[2,89],129:[2,89],132:[2,89],133:[2,89],134:[2,89],135:[2,89],136:[2,89],137:[2,89]},{10:165,27:166,28:[1,71],29:167,30:[1,69],31:[1,70],41:311,42:164,44:168,46:[1,44],89:[1,109]},{6:[2,90],10:165,25:[2,90],26:[2,90],27:166,28:[1,71],29:167,30:[1,69],31:[1,70],41:163,42:164,44:168,46:[1,44],54:[2,90],77:312,89:[1,109]},{6:[2,92],25:[2,92],26:[2,92],54:[2,92],78:[2,92]},{6:[2,39],25:[2,39],26:[2,39],54:[2,39],78:[2,39],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{7:313,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{73:[2,119],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,37],6:[2,37],25:[2,37],26:[2,37],49:[2,37],54:[2,37],57:[2,37],73:[2,37],78:[2,37],86:[2,37],91:[2,37],93:[2,37],102:[2,37],104:[2,37],105:[2,37],106:[2,37],110:[2,37],118:[2,37],126:[2,37],128:[2,37],129:[2,37],132:[2,37],133:[2,37],134:[2,37],135:[2,37],136:[2,37],137:[2,37]},{1:[2,110],6:[2,110],25:[2,110],26:[2,110],49:[2,110],54:[2,110],57:[2,110],66:[2,110],67:[2,110],68:[2,110],69:[2,110],71:[2,110],73:[2,110],74:[2,110],78:[2,110],84:[2,110],85:[2,110],86:[2,110],91:[2,110],93:[2,110],102:[2,110],104:[2,110],105:[2,110],106:[2,110],110:[2,110],118:[2,110],126:[2,110],128:[2,110],129:[2,110],132:[2,110],133:[2,110],134:[2,110],135:[2,110],136:[2,110],137:[2,110]},{1:[2,48],6:[2,48],25:[2,48],26:[2,48],49:[2,48],54:[2,48],57:[2,48],73:[2,48],78:[2,48],86:[2,48],91:[2,48],93:[2,48],102:[2,48],104:[2,48],105:[2,48],106:[2,48],110:[2,48],118:[2,48],126:[2,48],128:[2,48],129:[2,48],132:[2,48],133:[2,48],134:[2,48],135:[2,48],136:[2,48],137:[2,48]},{6:[2,57],25:[2,57],26:[2,57],49:[2,57],54:[2,57]},{6:[2,52],25:[2,52],26:[2,52],53:314,54:[1,199]},{1:[2,202],6:[2,202],25:[2,202],26:[2,202],49:[2,202],54:[2,202],57:[2,202],73:[2,202],78:[2,202],86:[2,202],91:[2,202],93:[2,202],102:[2,202],104:[2,202],105:[2,202],106:[2,202],110:[2,202],118:[2,202],126:[2,202],128:[2,202],129:[2,202],132:[2,202],133:[2,202],134:[2,202],135:[2,202],136:[2,202],137:[2,202]},{1:[2,181],6:[2,181],25:[2,181],26:[2,181],49:[2,181],54:[2,181],57:[2,181],73:[2,181],78:[2,181],86:[2,181],91:[2,181],93:[2,181],102:[2,181],104:[2,181],105:[2,181],106:[2,181],110:[2,181],118:[2,181],121:[2,181],126:[2,181],128:[2,181],129:[2,181],132:[2,181],133:[2,181],134:[2,181],135:[2,181],136:[2,181],137:[2,181]},{1:[2,135],6:[2,135],25:[2,135],26:[2,135],49:[2,135],54:[2,135],57:[2,135],73:[2,135],78:[2,135],86:[2,135],91:[2,135],93:[2,135],102:[2,135],104:[2,135],105:[2,135],106:[2,135],110:[2,135],118:[2,135],126:[2,135],128:[2,135],129:[2,135],132:[2,135],133:[2,135],134:[2,135],135:[2,135],136:[2,135],137:[2,135]},{1:[2,136],6:[2,136],25:[2,136],26:[2,136],49:[2,136],54:[2,136],57:[2,136],73:[2,136],78:[2,136],86:[2,136],91:[2,136],93:[2,136],98:[2,136],102:[2,136],104:[2,136],105:[2,136],106:[2,136],110:[2,136],118:[2,136],126:[2,136],128:[2,136],129:[2,136],132:[2,136],133:[2,136],134:[2,136],135:[2,136],136:[2,136],137:[2,136]},{1:[2,137],6:[2,137],25:[2,137],26:[2,137],49:[2,137],54:[2,137],57:[2,137],73:[2,137],78:[2,137],86:[2,137],91:[2,137],93:[2,137],98:[2,137],102:[2,137],104:[2,137],105:[2,137],106:[2,137],110:[2,137],118:[2,137],126:[2,137],128:[2,137],129:[2,137],132:[2,137],133:[2,137],134:[2,137],135:[2,137],136:[2,137],137:[2,137]},{1:[2,172],6:[2,172],25:[2,172],26:[2,172],49:[2,172],54:[2,172],57:[2,172],73:[2,172],78:[2,172],86:[2,172],91:[2,172],93:[2,172],102:[2,172],104:[2,172],105:[2,172],106:[2,172],110:[2,172],118:[2,172],126:[2,172],128:[2,172],129:[2,172],132:[2,172],133:[2,172],134:[2,172],135:[2,172],136:[2,172],137:[2,172]},{24:315,25:[1,112]},{26:[1,316]},{6:[1,317],26:[2,178],121:[2,178],123:[2,178]},{7:318,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{1:[2,102],6:[2,102],25:[2,102],26:[2,102],49:[2,102],54:[2,102],57:[2,102],73:[2,102],78:[2,102],86:[2,102],91:[2,102],93:[2,102],102:[2,102],104:[2,102],105:[2,102],106:[2,102],110:[2,102],118:[2,102],126:[2,102],128:[2,102],129:[2,102],132:[2,102],133:[2,102],134:[2,102],135:[2,102],136:[2,102],137:[2,102]},{1:[2,141],6:[2,141],25:[2,141],26:[2,141],49:[2,141],54:[2,141],57:[2,141],66:[2,141],67:[2,141],68:[2,141],69:[2,141],71:[2,141],73:[2,141],74:[2,141],78:[2,141],84:[2,141],85:[2,141],86:[2,141],91:[2,141],93:[2,141],102:[2,141],104:[2,141],105:[2,141],106:[2,141],110:[2,141],118:[2,141],126:[2,141],128:[2,141],129:[2,141],132:[2,141],133:[2,141],134:[2,141],135:[2,141],136:[2,141],137:[2,141]},{1:[2,118],6:[2,118],25:[2,118],26:[2,118],49:[2,118],54:[2,118],57:[2,118],66:[2,118],67:[2,118],68:[2,118],69:[2,118],71:[2,118],73:[2,118],74:[2,118],78:[2,118],84:[2,118],85:[2,118],86:[2,118],91:[2,118],93:[2,118],102:[2,118],104:[2,118],105:[2,118],106:[2,118],110:[2,118],118:[2,118],126:[2,118],128:[2,118],129:[2,118],132:[2,118],133:[2,118],134:[2,118],135:[2,118],136:[2,118],137:[2,118]},{6:[2,125],25:[2,125],26:[2,125],54:[2,125],86:[2,125],91:[2,125]},{6:[2,52],25:[2,52],26:[2,52],53:319,54:[1,226]},{6:[2,126],25:[2,126],26:[2,126],54:[2,126],86:[2,126],91:[2,126]},{1:[2,167],6:[2,167],25:[2,167],26:[2,167],49:[2,167],54:[2,167],57:[2,167],73:[2,167],78:[2,167],86:[2,167],91:[2,167],93:[2,167],102:[2,167],103:82,104:[2,167],105:[2,167],106:[2,167],109:83,110:[2,167],111:67,118:[1,320],126:[2,167],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,169],6:[2,169],25:[2,169],26:[2,169],49:[2,169],54:[2,169],57:[2,169],73:[2,169],78:[2,169],86:[2,169],91:[2,169],93:[2,169],102:[2,169],103:82,104:[2,169],105:[1,321],106:[2,169],109:83,110:[2,169],111:67,118:[2,169],126:[2,169],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,168],6:[2,168],25:[2,168],26:[2,168],49:[2,168],54:[2,168],57:[2,168],73:[2,168],78:[2,168],86:[2,168],91:[2,168],93:[2,168],102:[2,168],103:82,104:[2,168],105:[2,168],106:[2,168],109:83,110:[2,168],111:67,118:[2,168],126:[2,168],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[2,93],25:[2,93],26:[2,93],54:[2,93],78:[2,93]},{6:[2,52],25:[2,52],26:[2,52],53:322,54:[1,236]},{26:[1,323],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[1,247],25:[1,248],26:[1,324]},{26:[1,325]},{1:[2,175],6:[2,175],25:[2,175],26:[2,175],49:[2,175],54:[2,175],57:[2,175],73:[2,175],78:[2,175],86:[2,175],91:[2,175],93:[2,175],102:[2,175],104:[2,175],105:[2,175],106:[2,175],110:[2,175],118:[2,175],126:[2,175],128:[2,175],129:[2,175],132:[2,175],133:[2,175],134:[2,175],135:[2,175],136:[2,175],137:[2,175]},{26:[2,179],121:[2,179],123:[2,179]},{25:[2,131],54:[2,131],103:82,104:[1,63],106:[1,64],109:83,110:[1,66],111:67,126:[1,81],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[1,270],25:[1,271],26:[1,326]},{7:327,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{7:328,8:114,9:18,10:19,11:[1,20],12:6,13:7,14:8,15:9,16:10,17:11,18:12,19:13,20:14,21:15,22:16,23:17,27:60,28:[1,71],29:47,30:[1,69],31:[1,70],32:22,33:[1,48],34:[1,49],35:[1,50],36:[1,51],37:[1,52],38:[1,53],39:21,44:61,45:[1,43],46:[1,44],47:[1,27],50:28,51:[1,58],52:[1,59],58:45,59:46,61:34,63:23,64:24,65:25,76:[1,68],79:[1,41],83:[1,26],88:[1,56],89:[1,57],90:[1,55],96:[1,36],100:[1,42],101:[1,54],103:37,104:[1,63],106:[1,64],107:38,108:[1,65],109:39,110:[1,66],111:67,119:[1,40],124:35,125:[1,62],127:[1,29],128:[1,30],129:[1,31],130:[1,32],131:[1,33]},{6:[1,281],25:[1,282],26:[1,329]},{6:[2,40],25:[2,40],26:[2,40],54:[2,40],78:[2,40]},{6:[2,58],25:[2,58],26:[2,58],49:[2,58],54:[2,58]},{1:[2,173],6:[2,173],25:[2,173],26:[2,173],49:[2,173],54:[2,173],57:[2,173],73:[2,173],78:[2,173],86:[2,173],91:[2,173],93:[2,173],102:[2,173],104:[2,173],105:[2,173],106:[2,173],110:[2,173],118:[2,173],126:[2,173],128:[2,173],129:[2,173],132:[2,173],133:[2,173],134:[2,173],135:[2,173],136:[2,173],137:[2,173]},{6:[2,127],25:[2,127],26:[2,127],54:[2,127],86:[2,127],91:[2,127]},{1:[2,170],6:[2,170],25:[2,170],26:[2,170],49:[2,170],54:[2,170],57:[2,170],73:[2,170],78:[2,170],86:[2,170],91:[2,170],93:[2,170],102:[2,170],103:82,104:[2,170],105:[2,170],106:[2,170],109:83,110:[2,170],111:67,118:[2,170],126:[2,170],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{1:[2,171],6:[2,171],25:[2,171],26:[2,171],49:[2,171],54:[2,171],57:[2,171],73:[2,171],78:[2,171],86:[2,171],91:[2,171],93:[2,171],102:[2,171],103:82,104:[2,171],105:[2,171],106:[2,171],109:83,110:[2,171],111:67,118:[2,171],126:[2,171],128:[1,75],129:[1,74],132:[1,73],133:[1,76],134:[1,77],135:[1,78],136:[1,79],137:[1,80]},{6:[2,94],25:[2,94],26:[2,94],54:[2,94],78:[2,94]}],\n
defaultActions: {58:[2,50],59:[2,51],89:[2,108],186:[2,88]},\n
parseError: function parseError(str, hash) {\n
    if (hash.recoverable) {\n
        this.trace(str);\n
    } else {\n
        var e = new Error(str)\n
        e.location = hash.loc\n
        throw e;\n
    }\n
},\n
parse: function parse(input) {\n
    var self = this, stack = [0], vstack = [null], lstack = [], table = this.table, yytext = \'\', yylineno = 0, yyleng = 0, recovering = 0, TERROR = 2, EOF = 1;\n
    this.lexer.setInput(input);\n
    this.lexer.yy = this.yy;\n
    this.yy.lexer = this.lexer;\n
    this.yy.parser = this;\n
    if (typeof this.lexer.yylloc == \'undefined\') {\n
        this.lexer.yylloc = {};\n
    }\n
    var yyloc = this.lexer.yylloc;\n
    lstack.push(yyloc);\n
    var ranges = this.lexer.options && this.lexer.options.ranges;\n
    if (typeof this.yy.parseError === \'function\') {\n
        this.parseError = this.yy.parseError;\n
    } else {\n
        this.parseError = Object.getPrototypeOf(this).parseError;\n
    }\n
    function popStack(n) {\n
        stack.length = stack.length - 2 * n;\n
        vstack.length = vstack.length - n;\n
        lstack.length = lstack.length - n;\n
    }\n
    function lex() {\n
        var token;\n
        token = self.lexer.lex() || EOF;\n
        if (typeof token !== \'number\') {\n
            token = self.symbols_[token] || token;\n
        }\n
        return token;\n
    }\n
    var symbol, preErrorSymbol, state, action, a, r, yyval = {}, p, len, newState, expected;\n
    while (true) {\n
        state = stack[stack.length - 1];\n
        if (this.defaultActions[state]) {\n
            action = this.defaultActions[state];\n
        } else {\n
            if (symbol === null || typeof symbol == \'undefined\') {\n
                symbol = lex();\n
            }\n
            action = table[state] && table[state][symbol];\n
        }\n
                    if (typeof action === \'undefined\' || !action.length || !action[0]) {\n
                var errStr = \'\';\n
                expected = [];\n
                for (p in table[state]) {\n
                    if (this.terminals_[p] && p > TERROR) {\n
                        expected.push(\'\\\'\' + this.terminals_[p] + \'\\\'\');\n
                    }\n
                }\n
                if (this.lexer.showPosition) {\n
                    errStr = \'Expecting \' + expected.join(\', \') + \', got \\\'\' + (this.terminals_[symbol] || symbol) + \'\\\'\';\n
                } else {\n
                    errStr = \'Unexpected \' + (symbol == EOF ? \'end of input\' : \'\\\'\' + (this.terminals_[symbol] || symbol) + \'\\\'\');\n
                }\n
                if (this.lexer.yylloc.first_line !== yyloc.first_line) yyloc = this.lexer.yylloc;\n
                this.parseError(errStr, {\n
                    text: this.lexer.match,\n
                    token: this.terminals_[symbol] || symbol,\n
                    line: this.lexer.yylineno,\n
                    loc: yyloc,\n
                    expected: expected\n
                });\n
            }\n
        if (action[0] instanceof Array && action.length > 1) {\n
            throw new Error(\'Parse Error: multiple actions possible at state: \' + state + \', token: \' + symbol);\n
        }\n
        switch (action[0]) {\n
        case 1:\n
            stack.push(symbol);\n
            vstack.push(this.lexer.yytext);\n
            lstack.push(this.lexer.yylloc);\n
            stack.push(action[1]);\n
            symbol = null;\n
            if (!preErrorSymbol) {\n
                yyleng = this.lexer.yyleng;\n
                yytext = this.lexer.yytext;\n
                yylineno = this.lexer.yylineno;\n
                yyloc = this.lexer.yylloc;\n
                if (recovering > 0) {\n
                    recovering--;\n
                }\n
            } else {\n
                symbol = preErrorSymbol;\n
                preErrorSymbol = null;\n
            }\n
            break;\n
        case 2:\n
            len = this.productions_[action[1]][1];\n
            yyval.$ = vstack[vstack.length - len];\n
            yyval._$ = {\n
                first_line: lstack[lstack.length - (len || 1)].first_line,\n
                last_line: lstack[lstack.length - 1].last_line,\n
                first_column: lstack[lstack.length - (len || 1)].first_column,\n
                last_column: lstack[lstack.length - 1].last_column\n
            };\n
            if (ranges) {\n
                yyval._$.range = [\n
                    lstack[lstack.length - (len || 1)].range[0],\n
                    lstack[lstack.length - 1].range[1]\n
                ];\n
            }\n
            r = this.performAction.call(yyval, yytext, yyleng, yylineno, this.yy, action[1], vstack, lstack);\n
            if (typeof r !== \'undefined\') {\n
                return r;\n
            }\n
            if (len) {\n
                stack = stack.slice(0, -1 * len * 2);\n
                vstack = vstack.slice(0, -1 * len);\n
                lstack = lstack.slice(0, -1 * len);\n
            }\n
            stack.push(this.productions_[action[1]][0]);\n
            vstack.push(yyval.$);\n
            lstack.push(yyval._$);\n
            newState = table[stack[stack.length - 2]][stack[stack.length - 1]];\n
            stack.push(newState);\n
            break;\n
        case 3:\n
            return true;\n
        }\n
    }\n
    return true;\n
}};\n
undefined\n
function Parser () {\n
  this.yy = {};\n
}\n
Parser.prototype = parser;parser.Parser = Parser;\n
\n
module.exports = new Parser;\n
\n
\n
});\n
\n
define(\'ace/mode/coffee/nodes\', [\'require\', \'exports\', \'module\' , \'ace/mode/coffee/scope\', \'ace/mode/coffee/lexer\', \'ace/mode/coffee/helpers\'], function(require, exports, module) {\n
\n
  var Access, Arr, Assign, Base, Block, Call, Class, Closure, Code, CodeFragment, Comment, Existence, Extends, For, IDENTIFIER, IDENTIFIER_STR, IS_STRING, If, In, Index, LEVEL_ACCESS, LEVEL_COND, LEVEL_LIST, LEVEL_OP, LEVEL_PAREN, LEVEL_TOP, Literal, METHOD_DEF, NEGATE, NO, Obj, Op, Param, Parens, RESERVED, Range, Return, SIMPLENUM, STRICT_PROSCRIBED, Scope, Slice, Splat, Switch, TAB, THIS, Throw, Try, UTILITIES, Value, While, YES, addLocationDataFn, compact, del, ends, extend, flatten, fragmentsToText, last, locationDataToString, merge, multident, some, starts, throwSyntaxError, unfoldSoak, utility, _ref, _ref1, _ref2, _ref3,\n
    __hasProp = {}.hasOwnProperty,\n
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },\n
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; },\n
    __slice = [].slice;\n
\n
  Error.stackTraceLimit = Infinity;\n
\n
  Scope = require(\'./scope\').Scope;\n
\n
  _ref = require(\'./lexer\'), RESERVED = _ref.RESERVED, STRICT_PROSCRIBED = _ref.STRICT_PROSCRIBED;\n
\n
  _ref1 = require(\'./helpers\'), compact = _ref1.compact, flatten = _ref1.flatten, extend = _ref1.extend, merge = _ref1.merge, del = _ref1.del, starts = _ref1.starts, ends = _ref1.ends, last = _ref1.last, some = _ref1.some, addLocationDataFn = _ref1.addLocationDataFn, locationDataToString = _ref1.locationDataToString, throwSyntaxError = _ref1.throwSyntaxError;\n
\n
  exports.extend = extend;\n
\n
  exports.addLocationDataFn = addLocationDataFn;\n
\n
  YES = function() {\n
    return true;\n
  };\n
\n
  NO = function() {\n
    return false;\n
  };\n
\n
  THIS = function() {\n
    return this;\n
  };\n
\n
  NEGATE = function() {\n
    this.negated = !this.negated;\n
    return this;\n
  };\n
\n
  exports.CodeFragment = CodeFragment = (function() {\n
    function CodeFragment(parent, code) {\n
      var _ref2;\n
      this.code = "" + code;\n
      this.locationData = parent != null ? parent.locationData : void 0;\n
      this.type = (parent != null ? (_ref2 = parent.constructor) != null ? _ref2.name : void 0 : void 0) || \'unknown\';\n
    }\n
\n
    CodeFragment.prototype.toString = function() {\n
      return "" + this.code + (this.locationData ? ": " + locationDataToString(this.locationData) : \'\');\n
    };\n
\n
    return CodeFragment;\n
\n
  })();\n
\n
  fragmentsToText = function(fragments) {\n
    var fragment;\n
    return ((function() {\n
      var _i, _len, _results;\n
      _results = [];\n
      for (_i = 0, _len = fragments.length; _i < _len; _i++) {\n
        fragment = fragments[_i];\n
        _results.push(fragment.code);\n
      }\n
      return _results;\n
    })()).join(\'\');\n
  };\n
\n
  exports.Base = Base = (function() {\n
    function Base() {}\n
\n
    Base.prototype.compile = function(o, lvl) {\n
      return fragmentsToText(this.compileToFragments(o, lvl));\n
    };\n
\n
    Base.prototype.compileToFragments = function(o, lvl) {\n
      var node;\n
      o = extend({}, o);\n
      if (lvl) {\n
        o.level = lvl;\n
      }\n
      node = this.unfoldSoak(o) || this;\n
      node.tab = o.indent;\n
      if (o.level === LEVEL_TOP || !node.isStatement(o)) {\n
        return node.compileNode(o);\n
      } else {\n
        return node.compileClosure(o);\n
      }\n
    };\n
\n
    Base.prototype.compileClosure = function(o) {\n
      var jumpNode;\n
      if (jumpNode = this.jumps()) {\n
        jumpNode.error(\'cannot use a pure statement in an expression\');\n
      }\n
      o.sharedScope = true;\n
      return Closure.wrap(this).compileNode(o);\n
    };\n
\n
    Base.prototype.cache = function(o, level, reused) {\n
      var ref, sub;\n
      if (!this.isComplex()) {\n
        ref = level ? this.compileToFragments(o, level) : this;\n
        return [ref, ref];\n
      } else {\n
        ref = new Literal(reused || o.scope.freeVariable(\'ref\'));\n
        sub = new Assign(ref, this);\n
        if (level) {\n
          return [sub.compileToFragments(o, level), [this.makeCode(ref.value)]];\n
        } else {\n
          return [sub, ref];\n
        }\n
      }\n
    };\n
\n
    Base.prototype.cacheToCodeFragments = function(cacheValues) {\n
      return [fragmentsToText(cacheValues[0]), fragmentsToText(cacheValues[1])];\n
    };\n
\n
    Base.prototype.makeReturn = function(res) {\n
      var me;\n
      me = this.unwrapAll();\n
      if (res) {\n
        return new Call(new Literal("" + res + ".push"), [me]);\n
      } else {\n
        return new Return(me);\n
      }\n
    };\n
\n
    Base.prototype.contains = function(pred) {\n
      var node;\n
      node = void 0;\n
      this.traverseChildren(false, function(n) {\n
        if (pred(n)) {\n
          node = n;\n
          return false;\n
        }\n
      });\n
      return node;\n
    };\n
\n
    Base.prototype.lastNonComment = function(list) {\n
      var i;\n
      i = list.length;\n
      while (i--) {\n
        if (!(list[i] instanceof Comment)) {\n
          return list[i];\n
        }\n
      }\n
      return null;\n
    };\n
\n
    Base.prototype.toString = function(idt, name) {\n
      var tree;\n
      if (idt == null) {\n
        idt = \'\';\n
      }\n
      if (name == null) {\n
        name = this.constructor.name;\n
      }\n
      tree = \'\\n\' + idt + name;\n
      if (this.soak) {\n
        tree += \'?\';\n
      }\n
      this.eachChild(function(node) {\n
        return tree += node.toString(idt + TAB);\n
      });\n
      return tree;\n
    };\n
\n
    Base.prototype.eachChild = function(func) {\n
      var attr, child, _i, _j, _len, _len1, _ref2, _ref3;\n
      if (!this.children) {\n
        return this;\n
      }\n
      _ref2 = this.children;\n
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {\n
        attr = _ref2[_i];\n
        if (this[attr]) {\n
          _ref3 = flatten([this[attr]]);\n
          for (_j = 0, _len1 = _ref3.length; _j < _len1; _j++) {\n
            child = _ref3[_j];\n
            if (func(child) === false) {\n
              return this;\n
            }\n
          }\n
        }\n
      }\n
      return this;\n
    };\n
\n
    Base.prototype.traverseChildren = function(crossScope, func) {\n
      return this.eachChild(function(child) {\n
        var recur;\n
        recur = func(child);\n
        if (recur !== false) {\n
          return child.traverseChildren(crossScope, func);\n
        }\n
      });\n
    };\n
\n
    Base.prototype.invert = function() {\n
      return new Op(\'!\', this);\n
    };\n
\n
    Base.prototype.unwrapAll = function() {\n
      var node;\n
      node = this;\n
      while (node !== (node = node.unwrap())) {\n
        continue;\n
      }\n
      return node;\n
    };\n
\n
    Base.prototype.children = [];\n
\n
    Base.prototype.isStatement = NO;\n
\n
    Base.prototype.jumps = NO;\n
\n
    Base.prototype.isComplex = YES;\n
\n
    Base.prototype.isChainable = NO;\n
\n
    Base.prototype.isAssignable = NO;\n
\n
    Base.prototype.unwrap = THIS;\n
\n
    Base.prototype.unfoldSoak = NO;\n
\n
    Base.prototype.assigns = NO;\n
\n
    Base.prototype.updateLocationDataIfMissing = function(locationData) {\n
      if (this.locationData) {\n
        return this;\n
      }\n
      this.locationData = locationData;\n
      return this.eachChild(function(child) {\n
        return child.updateLocationDataIfMissing(locationData);\n
      });\n
    };\n
\n
    Base.prototype.error = function(message) {\n
      return throwSyntaxError(message, this.locationData);\n
    };\n
\n
    Base.prototype.makeCode = function(code) {\n
      return new CodeFragment(this, code);\n
    };\n
\n
    Base.prototype.wrapInBraces = function(fragments) {\n
      return [].concat(this.makeCode(\'(\'), fragments, this.makeCode(\')\'));\n
    };\n
\n
    Base.prototype.joinFragmentArrays = function(fragmentsList, joinStr) {\n
      var answer, fragments, i, _i, _len;\n
      answer = [];\n
      for (i = _i = 0, _len = fragmentsList.length; _i < _len; i = ++_i) {\n
        fragments = fragmentsList[i];\n
        if (i) {\n
          answer.push(this.makeCode(joinStr));\n
        }\n
        answer = answer.concat(fragments);\n
      }\n
      return answer;\n
    };\n
\n
    return Base;\n
\n
  })();\n
\n
  exports.Block = Block = (function(_super) {\n
    __extends(Block, _super);\n
\n
    function Block(nodes) {\n
      this.expressions = compact(flatten(nodes || []));\n
    }\n
\n
    Block.prototype.children = [\'expressions\'];\n
\n
    Block.prototype.push = function(node) {\n
      this.expressions.push(node);\n
      return this;\n
    };\n
\n
    Block.prototype.pop = function() {\n
      return this.expressions.pop();\n
    };\n
\n
    Block.prototype.unshift = function(node) {\n
      this.expressions.unshift(node);\n
      return this;\n
    };\n
\n
    Block.prototype.unwrap = function() {\n
      if (this.expressions.length === 1) {\n
        return this.expressions[0];\n
      } else {\n
        return this;\n
      }\n
    };\n
\n
    Block.prototype.isEmpty = function() {\n
      return !this.expressions.length;\n
    };\n
\n
    Block.prototype.isStatement = function(o) {\n
      var exp, _i, _len, _ref2;\n
      _ref2 = this.expressions;\n
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {\n
        exp = _ref2[_i];\n
        if (exp.isStatement(o)) {\n
          return true;\n
        }\n
      }\n
      return false;\n
    };\n
\n
    Block.prototype.jumps = function(o) {\n
      var exp, _i, _len, _ref2;\n
      _ref2 = this.expressions;\n
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {\n
        exp = _ref2[_i];\n
        if (exp.jumps(o)) {\n
          return exp;\n
        }\n
      }\n
    };\n
\n
    Block.prototype.makeReturn = function(res) {\n
      var expr, len;\n
      len = this.expressions.length;\n
      while (len--) {\n
        expr = this.expressions[len];\n
        if (!(expr instanceof Comment)) {\n
          this.expressions[len] = expr.makeReturn(res);\n
          if (expr instanceof Return && !expr.expression) {\n
            this.expressions.splice(len, 1);\n
          }\n
          break;\n
        }\n
      }\n
      return this;\n
    };\n
\n
    Block.prototype.compileToFragments = function(o, level) {\n
      if (o == null) {\n
        o = {};\n
      }\n
      if (o.scope) {\n
        return Block.__super__.compileToFragments.call(this, o, level);\n
      } else {\n
        return this.compileRoot(o);\n
      }\n
    };\n
\n
    Block.prototype.compileNode = function(o) {\n
      var answer, compiledNodes, fragments, index, node, top, _i, _len, _ref2;\n
      this.tab = o.indent;\n
      top = o.level === LEVEL_TOP;\n
      compiledNodes = [];\n
      _ref2 = this.expressions;\n
      for (index = _i = 0, _len = _ref2.length; _i < _len; index = ++_i) {\n
        node = _ref2[index];\n
        node = node.unwrapAll();\n
        node = node.unfoldSoak(o) || node;\n
        if (node instanceof Block) {\n
          compiledNodes.push(node.compileNode(o));\n
        } else if (top) {\n
          node.front = true;\n
          fragments = node.compileToFragments(o);\n
          if (!node.isStatement(o)) {\n
            fragments.unshift(this.makeCode("" + this.tab));\n
            fragments.push(this.makeCode(";"));\n
          }\n
          compiledNodes.push(fragments);\n
        } else {\n
          compiledNodes.push(node.compileToFragments(o, LEVEL_LIST));\n
        }\n
      }\n
      if (top) {\n
        if (this.spaced) {\n
          return [].concat(this.joinFragmentArrays(compiledNodes, \'\\n\\n\'), this.makeCode("\\n"));\n
        } else {\n
          return this.joinFragmentArrays(compiledNodes, \'\\n\');\n
        }\n
      }\n
      if (compiledNodes.length) {\n
        answer = this.joinFragmentArrays(compiledNodes, \', \');\n
      } else {\n
        answer = [this.makeCode("void 0")];\n
      }\n
      if (compiledNodes.length > 1 && o.level >= LEVEL_LIST) {\n
        return this.wrapInBraces(answer);\n
      } else {\n
        return answer;\n
      }\n
    };\n
\n
    Block.prototype.compileRoot = function(o) {\n
      var exp, fragments, i, name, prelude, preludeExps, rest, _i, _len, _ref2;\n
      o.indent = o.bare ? \'\' : TAB;\n
      o.level = LEVEL_TOP;\n
      this.spaced = true;\n
      o.scope = new Scope(null, this, null);\n
      _ref2 = o.locals || [];\n
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {\n
        name = _ref2[_i];\n
        o.scope.parameter(name);\n
      }\n
      prelude = [];\n
      if (!o.bare) {\n
        preludeExps = (function() {\n
          var _j, _len1, _ref3, _results;\n
          _ref3 = this.expressions;\n
          _results = [];\n
          for (i = _j = 0, _len1 = _ref3.length; _j < _len1; i = ++_j) {\n
            exp = _ref3[i];\n
            if (!(exp.unwrap() instanceof Comment)) {\n
              break;\n
            }\n
            _results.push(exp);\n
          }\n
          return _results;\n
        }).call(this);\n
        rest = this.expressions.slice(preludeExps.length);\n
        this.expressions = preludeExps;\n
        if (preludeExps.length) {\n
          prelude = this.compileNode(merge(o, {\n
            indent: \'\'\n
          }));\n
          prelude.push(this.makeCode("\\n"));\n
        }\n
        this.expressions = rest;\n
      }\n
      fragments = this.compileWithDeclarations(o);\n
      if (o.bare) {\n
        return fragments;\n
      }\n
      return [].concat(prelude, this.makeCode("(function() {\\n"), fragments, this.makeCode("\\n}).call(this);\\n"));\n
    };\n
\n
    Block.prototype.compileWithDeclarations = function(o) {\n
      var assigns, declars, exp, fragments, i, post, rest, scope, spaced, _i, _len, _ref2, _ref3, _ref4;\n
      fragments = [];\n
      post = [];\n
      _ref2 = this.expressions;\n
      for (i = _i = 0, _len = _ref2.length; _i < _len; i = ++_i) {\n
        exp = _ref2[i];\n
        exp = exp.unwrap();\n
        if (!(exp instanceof Comment || exp instanceof Literal)) {\n
          break;\n
        }\n
      }\n
      o = merge(o, {\n
        level: LEVEL_TOP\n
      });\n
      if (i) {\n
        rest = this.expressions.splice(i, 9e9);\n
        _ref3 = [this.spaced, false], spaced = _ref3[0], this.spaced = _ref3[1];\n
        _ref4 = [this.compileNode(o), spaced], fragments = _ref4[0], this.spaced = _ref4[1];\n
        this.expressions = rest;\n
      }\n
      post = this.compileNode(o);\n
      scope = o.scope;\n
      if (scope.expressions === this) {\n
        declars = o.scope.hasDeclarations();\n
        assigns = scope.hasAssignments;\n
        if (declars || assigns) {\n
          if (i) {\n
            fragments.push(this.makeCode(\'\\n\'));\n
          }\n
          fragments.push(this.makeCode("" + this.tab + "var "));\n
          if (declars) {\n
            fragments.push(this.makeCode(scope.declaredVariables().join(\', \')));\n
          }\n
          if (assigns) {\n
            if (declars) {\n
              fragments.push(this.makeCode(",\\n" + (this.tab + TAB)));\n
            }\n
            fragments.push(this.makeCode(scope.assignedVariables().join(",\\n" + (this.tab + TAB))));\n
          }\n
          fragments.push(this.makeCode(";\\n" + (this.spaced ? \'\\n\' : \'\')));\n
        } else if (fragments.length && post.length) {\n
          fragments.push(this.makeCode("\\n"));\n
        }\n
      }\n
      return fragments.concat(post);\n
    };\n
\n
    Block.wrap = function(nodes) {\n
      if (nodes.length === 1 && nodes[0] instanceof Block) {\n
        return nodes[0];\n
      }\n
      return new Block(nodes);\n
    };\n
\n
    return Block;\n
\n
  })(Base);\n
\n
  exports.Literal = Literal = (function(_super) {\n
    __extends(Literal, _super);\n
\n
    function Literal(value) {\n
      this.value = value;\n
    }\n
\n
    Literal.prototype.makeReturn = function() {\n
      if (this.isStatement()) {\n
        return this;\n
      } else {\n
        return Literal.__super__.makeReturn.apply(this, arguments);\n
      }\n
    };\n
\n
    Literal.prototype.isAssignable = function() {\n
      return IDENTIFIER.test(this.value);\n
    };\n
\n
    Literal.prototype.isStatement = function() {\n
      var _ref2;\n
      return (_ref2 = this.value) === \'break\' || _ref2 === \'continue\' || _ref2 === \'debugger\';\n
    };\n
\n
    Literal.prototype.isComplex = NO;\n
\n
    Literal.prototype.assigns = function(name) {\n
      return name === this.value;\n
    };\n
\n
    Literal.prototype.jumps = function(o) {\n
      if (this.value === \'break\' && !((o != null ? o.loop : void 0) || (o != null ? o.block : void 0))) {\n
        return this;\n
      }\n
      if (this.value === \'continue\' && !(o != null ? o.loop : void 0)) {\n
        return this;\n
      }\n
    };\n
\n
    Literal.prototype.compileNode = function(o) {\n
      var answer, code, _ref2;\n
      code = this.value === \'this\' ? ((_ref2 = o.scope.method) != null ? _ref2.bound : void 0) ? o.scope.method.context : this.value : this.value.reserved ? "\\"" + this.value + "\\"" : this.value;\n
      answer = this.isStatement() ? "" + this.tab + code + ";" : code;\n
      return [this.makeCode(answer)];\n
    };\n
\n
    Literal.prototype.toString = function() {\n
      return \' "\' + this.value + \'"\';\n
    };\n
\n
    return Literal;\n
\n
  })(Base);\n
\n
  exports.Undefined = (function(_super) {\n
    __extends(Undefined, _super);\n
\n
    function Undefined() {\n
      _ref2 = Undefined.__super__.constructor.apply(this, arguments);\n
      return _ref2;\n
    }\n
\n
    Undefined.prototype.isAssignable = NO;\n
\n
    Undefined.prototype.isComplex = NO;\n
\n
    Undefined.prototype.compileNode = function(o) {\n
      return [this.makeCode(o.level >= LEVEL_ACCESS ? \'(void 0)\' : \'void 0\')];\n
    };\n
\n
    return Undefined;\n
\n
  })(Base);\n
\n
  exports.Null = (function(_super) {\n
    __extends(Null, _super);\n
\n
    function Null() {\n
      _ref3 = Null.__super__.constructor.apply(this, arguments);\n
      return _ref3;\n
    }\n
\n
    Null.prototype.isAssignable = NO;\n
\n
    Null.prototype.isComplex = NO;\n
\n
    Null.prototype.compileNode = function() {\n
      return [this.makeCode("null")];\n
    };\n
\n
    return Null;\n
\n
  })(Base);\n
\n
  exports.Bool = (function(_super) {\n
    __extends(Bool, _super);\n
\n
    Bool.prototype.isAssignable = NO;\n
\n
    Bool.prototype.isComplex = NO;\n
\n
    Bool.prototype.compileNode = function() {\n
      return [this.makeCode(this.val)];\n
    };\n
\n
    function Bool(val) {\n
      this.val = val;\n
    }\n
\n
    return Bool;\n
\n
  })(Base);\n
\n
  exports.Return = Return = (function(_super) {\n
    __extends(Return, _super);\n
\n
    function Return(expr) {\n
      if (expr && !expr.unwrap().isUndefined) {\n
        this.expression = expr;\n
      }\n
    }\n
\n
    Return.prototype.children = [\'expression\'];\n
\n
    Return.prototype.isStatement = YES;\n
\n
    Return.prototype.makeReturn = THIS;\n
\n
    Return.prototype.jumps = THIS;\n
\n
    Return.prototype.compileToFragments = function(o, level) {\n
      var expr, _ref4;\n
      expr = (_ref4 = this.expression) != null ? _ref4.makeReturn() : void 0;\n
      if (expr && !(expr instanceof Return)) {\n
        return expr.compileToFragments(o, level);\n
      } else {\n
        return Return.__super__.compileToFragments.call(this, o, level);\n
      }\n
    };\n
\n
    Return.prototype.compileNode = function(o) {\n
      var answer;\n
      answer = [];\n
      answer.push(this.makeCode(this.tab + ("return" + (this.expression ? " " : ""))));\n
      if (this.expression) {\n
        answer = answer.concat(this.expression.compileToFragments(o, LEVEL_PAREN));\n
      }\n
      answer.push(this.makeCode(";"));\n
      return answer;\n
    };\n
\n
    return Return;\n
\n
  })(Base);\n
\n
  exports.Value = Value = (function(_super) {\n
    __extends(Value, _super);\n
\n
    function Value(base, props, tag) {\n
      if (!props && base instanceof Value) {\n
        return base;\n
      }\n
      this.base = base;\n
      this.properties = props || [];\n
      if (tag) {\n
        this[tag] = true;\n
      }\n
      return this;\n
    }\n
\n
    Value.prototype.children = [\'base\', \'properties\'];\n
\n
    Value.prototype.add = function(props) {\n
      this.properties = this.properties.concat(props);\n
      return this;\n
    };\n
\n
    Value.prototype.hasProperties = function() {\n
      return !!this.properties.length;\n
    };\n
\n
    Value.prototype.isArray = function() {\n
      return !this.properties.length && this.base instanceof Arr;\n
    };\n
\n
    Value.prototype.isComplex = function() {\n
      return this.hasProperties() || this.base.isComplex();\n
    };\n
\n
    Value.prototype.isAssignable = function() {\n
      return this.hasProperties() || this.base.isAssignable();\n
    };\n
\n
    Value.prototype.isSimpleNumber = function() {\n
      return this.base instanceof Literal && SIMPLENUM.test(this.base.value);\n
    };\n
\n
    Value.prototype.isString = function() {\n
      return this.base instanceof Literal && IS_STRING.test(this.base.value);\n
    };\n
\n
    Value.prototype.isAtomic = function() {\n
      var node, _i, _len, _ref4;\n
      _ref4 = this.properties.concat(this.base);\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        node = _ref4[_i];\n
        if (node.soak || node instanceof Call) {\n
          return false;\n
        }\n
      }\n
      return true;\n
    };\n
\n
    Value.prototype.isStatement = function(o) {\n
      return !this.properties.length && this.base.isStatement(o);\n
    };\n
\n
    Value.prototype.assigns = function(name) {\n
      return !this.properties.length && this.base.assigns(name);\n
    };\n
\n
    Value.prototype.jumps = function(o) {\n
      return !this.properties.length && this.base.jumps(o);\n
    };\n
\n
    Value.prototype.isObject = function(onlyGenerated) {\n
      if (this.properties.length) {\n
        return false;\n
      }\n
      return (this.base instanceof Obj) && (!onlyGenerated || this.base.generated);\n
    };\n
\n
    Value.prototype.isSplice = function() {\n
      return last(this.properties) instanceof Slice;\n
    };\n
\n
    Value.prototype.unwrap = function() {\n
      if (this.properties.length) {\n
        return this;\n
      } else {\n
        return this.base;\n
      }\n
    };\n
\n
    Value.prototype.cacheReference = function(o) {\n
      var base, bref, name, nref;\n
      name = last(this.properties);\n
      if (this.properties.length < 2 && !this.base.isComplex() && !(name != null ? name.isComplex() : void 0)) {\n
        return [this, this];\n
      }\n
      base = new Value(this.base, this.properties.slice(0, -1));\n
      if (base.isComplex()) {\n
        bref = new Literal(o.scope.freeVariable(\'base\'));\n
        base = new Value(new Parens(new Assign(bref, base)));\n
      }\n
      if (!name) {\n
        return [base, bref];\n
      }\n
      if (name.isComplex()) {\n
        nref = new Literal(o.scope.freeVariable(\'name\'));\n
        name = new Index(new Assign(nref, name.index));\n
        nref = new Index(nref);\n
      }\n
      return [base.add(name), new Value(bref || base.base, [nref || name])];\n
    };\n
\n
    Value.prototype.compileNode = function(o) {\n
      var fragments, prop, props, _i, _len;\n
      this.base.front = this.front;\n
      props = this.properties;\n
      fragments = this.base.compileToFragments(o, (props.length ? LEVEL_ACCESS : null));\n
      if ((this.base instanceof Parens || props.length) && SIMPLENUM.test(fragmentsToText(fragments))) {\n
        fragments.push(this.makeCode(\'.\'));\n
      }\n
      for (_i = 0, _len = props.length; _i < _len; _i++) {\n
        prop = props[_i];\n
        fragments.push.apply(fragments, prop.compileToFragments(o));\n
      }\n
      return fragments;\n
    };\n
\n
    Value.prototype.unfoldSoak = function(o) {\n
      var _this = this;\n
      return this.unfoldedSoak != null ? this.unfoldedSoak : this.unfoldedSoak = (function() {\n
        var fst, i, ifn, prop, ref, snd, _i, _len, _ref4, _ref5;\n
        if (ifn = _this.base.unfoldSoak(o)) {\n
          (_ref4 = ifn.body.properties).push.apply(_ref4, _this.properties);\n
          return ifn;\n
        }\n
        _ref5 = _this.properties;\n
        for (i = _i = 0, _len = _ref5.length; _i < _len; i = ++_i) {\n
          prop = _ref5[i];\n
          if (!prop.soak) {\n
            continue;\n
          }\n
          prop.soak = false;\n
          fst = new Value(_this.base, _this.properties.slice(0, i));\n
          snd = new Value(_this.base, _this.properties.slice(i));\n
          if (fst.isComplex()) {\n
            ref = new Literal(o.scope.freeVariable(\'ref\'));\n
            fst = new Parens(new Assign(ref, fst));\n
            snd.base = ref;\n
          }\n
          return new If(new Existence(fst), snd, {\n
            soak: true\n
          });\n
        }\n
        return false;\n
      })();\n
    };\n
\n
    return Value;\n
\n
  })(Base);\n
\n
  exports.Comment = Comment = (function(_super) {\n
    __extends(Comment, _super);\n
\n
    function Comment(comment) {\n
      this.comment = comment;\n
    }\n
\n
    Comment.prototype.isStatement = YES;\n
\n
    Comment.prototype.makeReturn = THIS;\n
\n
    Comment.prototype.compileNode = function(o, level) {\n
      var code;\n
      code = "/*" + (multident(this.comment, this.tab)) + (__indexOf.call(this.comment, \'\\n\') >= 0 ? "\\n" + this.tab : \'\') + "*/";\n
      if ((level || o.level) === LEVEL_TOP) {\n
        code = o.indent + code;\n
      }\n
      return [this.makeCode("\\n"), this.makeCode(code)];\n
    };\n
\n
    return Comment;\n
\n
  })(Base);\n
\n
  exports.Call = Call = (function(_super) {\n
    __extends(Call, _super);\n
\n
    function Call(variable, args, soak) {\n
      this.args = args != null ? args : [];\n
      this.soak = soak;\n
      this.isNew = false;\n
      this.isSuper = variable === \'super\';\n
      this.variable = this.isSuper ? null : variable;\n
    }\n
\n
    Call.prototype.children = [\'variable\', \'args\'];\n
\n
    Call.prototype.newInstance = function() {\n
      var base, _ref4;\n
      base = ((_ref4 = this.variable) != null ? _ref4.base : void 0) || this.variable;\n
      if (base instanceof Call && !base.isNew) {\n
        base.newInstance();\n
      } else {\n
        this.isNew = true;\n
      }\n
      return this;\n
    };\n
\n
    Call.prototype.superReference = function(o) {\n
      var accesses, method;\n
      method = o.scope.namedMethod();\n
      if (method != null ? method.klass : void 0) {\n
        accesses = [new Access(new Literal(\'__super__\'))];\n
        if (method["static"]) {\n
          accesses.push(new Access(new Literal(\'constructor\')));\n
        }\n
        accesses.push(new Access(new Literal(method.name)));\n
        return (new Value(new Literal(method.klass), accesses)).compile(o);\n
      } else if (method != null ? method.ctor : void 0) {\n
        return "" + method.name + ".__super__.constructor";\n
      } else {\n
        return this.error(\'cannot call super outside of an instance method.\');\n
      }\n
    };\n
\n
    Call.prototype.superThis = function(o) {\n
      var method;\n
      method = o.scope.method;\n
      return (method && !method.klass && method.context) || "this";\n
    };\n
\n
    Call.prototype.unfoldSoak = function(o) {\n
      var call, ifn, left, list, rite, _i, _len, _ref4, _ref5;\n
      if (this.soak) {\n
        if (this.variable) {\n
          if (ifn = unfoldSoak(o, this, \'variable\')) {\n
            return ifn;\n
          }\n
          _ref4 = new Value(this.variable).cacheReference(o), left = _ref4[0], rite = _ref4[1];\n
        } else {\n
          left = new Literal(this.superReference(o));\n
          rite = new Value(left);\n
        }\n
        rite = new Call(rite, this.args);\n
        rite.isNew = this.isNew;\n
        left = new Literal("typeof " + (left.compile(o)) + " === \\"function\\"");\n
        return new If(left, new Value(rite), {\n
          soak: true\n
        });\n
      }\n
      call = this;\n
      list = [];\n
      while (true) {\n
        if (call.variable instanceof Call) {\n
          list.push(call);\n
          call = call.variable;\n
          continue;\n
        }\n
        if (!(call.variable instanceof Value)) {\n
          break;\n
        }\n
        list.push(call);\n
        if (!((call = call.variable.base) instanceof Call)) {\n
          break;\n
        }\n
      }\n
      _ref5 = list.reverse();\n
      for (_i = 0, _len = _ref5.length; _i < _len; _i++) {\n
        call = _ref5[_i];\n
        if (ifn) {\n
          if (call.variable instanceof Call) {\n
            call.variable = ifn;\n
          } else {\n
            call.variable.base = ifn;\n
          }\n
        }\n
        ifn = unfoldSoak(o, call, \'variable\');\n
      }\n
      return ifn;\n
    };\n
\n
    Call.prototype.compileNode = function(o) {\n
      var arg, argIndex, compiledArgs, compiledArray, fragments, preface, _i, _len, _ref4, _ref5;\n
      if ((_ref4 = this.variable) != null) {\n
        _ref4.front = this.front;\n
      }\n
      compiledArray = Splat.compileSplattedArray(o, this.args, true);\n
      if (compiledArray.length) {\n
        return this.compileSplat(o, compiledArray);\n
      }\n
      compiledArgs = [];\n
      _ref5 = this.args;\n
      for (argIndex = _i = 0, _len = _ref5.length; _i < _len; argIndex = ++_i) {\n
        arg = _ref5[argIndex];\n
        if (argIndex) {\n
          compiledArgs.push(this.makeCode(", "));\n
        }\n
        compiledArgs.push.apply(compiledArgs, arg.compileToFragments(o, LEVEL_LIST));\n
      }\n
      fragments = [];\n
      if (this.isSuper) {\n
        preface = this.superReference(o) + (".call(" + (this.superThis(o)));\n
        if (compiledArgs.length) {\n
          preface += ", ";\n
        }\n
        fragments.push(this.makeCode(preface));\n
      } else {\n
        if (this.isNew) {\n
          fragments.push(this.makeCode(\'new \'));\n
        }\n
        fragments.push.apply(fragments, this.variable.compileToFragments(o, LEVEL_ACCESS));\n
        fragments.push(this.makeCode("("));\n
      }\n
      fragments.push.apply(fragments, compiledArgs);\n
      fragments.push(this.makeCode(")"));\n
      return fragments;\n
    };\n
\n
    Call.prototype.compileSplat = function(o, splatArgs) {\n
      var answer, base, fun, idt, name, ref;\n
      if (this.isSuper) {\n
        return [].concat(this.makeCode("" + (this.superReference(o)) + ".apply(" + (this.superThis(o)) + ", "), splatArgs, this.makeCode(")"));\n
      }\n
      if (this.isNew) {\n
        idt = this.tab + TAB;\n
        return [].concat(this.makeCode("(function(func, args, ctor) {\\n" + idt + "ctor.prototype = func.prototype;\\n" + idt + "var child = new ctor, result = func.apply(child, args);\\n" + idt + "return Object(result) === result ? result : child;\\n" + this.tab + "})("), this.variable.compileToFragments(o, LEVEL_LIST), this.makeCode(", "), splatArgs, this.makeCode(", function(){})"));\n
      }\n
      answer = [];\n
      base = new Value(this.variable);\n
      if ((name = base.properties.pop()) && base.isComplex()) {\n
        ref = o.scope.freeVariable(\'ref\');\n
        answer = answer.concat(this.makeCode("(" + ref + " = "), base.compileToFragments(o, LEVEL_LIST), this.makeCode(")"), name.compileToFragments(o));\n
      } else {\n
        fun = base.compileToFragments(o, LEVEL_ACCESS);\n
        if (SIMPLENUM.test(fragmentsToText(fun))) {\n
          fun = this.wrapInBraces(fun);\n
        }\n
        if (name) {\n
          ref = fragmentsToText(fun);\n
          fun.push.apply(fun, name.compileToFragments(o));\n
        } else {\n
          ref = \'null\';\n
        }\n
        answer = answer.concat(fun);\n
      }\n
      return answer = answer.concat(this.makeCode(".apply(" + ref + ", "), splatArgs, this.makeCode(")"));\n
    };\n
\n
    return Call;\n
\n
  })(Base);\n
\n
  exports.Extends = Extends = (function(_super) {\n
    __extends(Extends, _super);\n
\n
    function Extends(child, parent) {\n
      this.child = child;\n
      this.parent = parent;\n
    }\n
\n
    Extends.prototype.children = [\'child\', \'parent\'];\n
\n
    Extends.prototype.compileToFragments = function(o) {\n
      return new Call(new Value(new Literal(utility(\'extends\'))), [this.child, this.parent]).compileToFragments(o);\n
    };\n
\n
    return Extends;\n
\n
  })(Base);\n
\n
  exports.Access = Access = (function(_super) {\n
    __extends(Access, _super);\n
\n
    function Access(name, tag) {\n
      this.name = name;\n
      this.name.asKey = true;\n
      this.soak = tag === \'soak\';\n
    }\n
\n
    Access.prototype.children = [\'name\'];\n
\n
    Access.prototype.compileToFragments = function(o) {\n
      var name;\n
      name = this.name.compileToFragments(o);\n
      if (IDENTIFIER.test(fragmentsToText(name))) {\n
        name.unshift(this.makeCode("."));\n
      } else {\n
        name.unshift(this.makeCode("["));\n
        name.push(this.makeCode("]"));\n
      }\n
      return name;\n
    };\n
\n
    Access.prototype.isComplex = NO;\n
\n
    return Access;\n
\n
  })(Base);\n
\n
  exports.Index = Index = (function(_super) {\n
    __extends(Index, _super);\n
\n
    function Index(index) {\n
      this.index = index;\n
    }\n
\n
    Index.prototype.children = [\'index\'];\n
\n
    Index.prototype.compileToFragments = function(o) {\n
      return [].concat(this.makeCode("["), this.index.compileToFragments(o, LEVEL_PAREN), this.makeCode("]"));\n
    };\n
\n
    Index.prototype.isComplex = function() {\n
      return this.index.isComplex();\n
    };\n
\n
    return Index;\n
\n
  })(Base);\n
\n
  exports.Range = Range = (function(_super) {\n
    __extends(Range, _super);\n
\n
    Range.prototype.children = [\'from\', \'to\'];\n
\n
    function Range(from, to, tag) {\n
      this.from = from;\n
      this.to = to;\n
      this.exclusive = tag === \'exclusive\';\n
      this.equals = this.exclusive ? \'\' : \'=\';\n
    }\n
\n
    Range.prototype.compileVariables = function(o) {\n
      var step, _ref4, _ref5, _ref6, _ref7;\n
      o = merge(o, {\n
        top: true\n
      });\n
      _ref4 = this.cacheToCodeFragments(this.from.cache(o, LEVEL_LIST)), this.fromC = _ref4[0], this.fromVar = _ref4[1];\n
      _ref5 = this.cacheToCodeFragments(this.to.cache(o, LEVEL_LIST)), this.toC = _ref5[0], this.toVar = _ref5[1];\n
      if (step = del(o, \'step\')) {\n
        _ref6 = this.cacheToCodeFragments(step.cache(o, LEVEL_LIST)), this.step = _ref6[0], this.stepVar = _ref6[1];\n
      }\n
      _ref7 = [this.fromVar.match(SIMPLENUM), this.toVar.match(SIMPLENUM)], this.fromNum = _ref7[0], this.toNum = _ref7[1];\n
      if (this.stepVar) {\n
        return this.stepNum = this.stepVar.match(SIMPLENUM);\n
      }\n
    };\n
\n
    Range.prototype.compileNode = function(o) {\n
      var cond, condPart, from, gt, idx, idxName, known, lt, namedIndex, stepPart, to, varPart, _ref4, _ref5;\n
      if (!this.fromVar) {\n
        this.compileVariables(o);\n
      }\n
      if (!o.index) {\n
        return this.compileArray(o);\n
      }\n
      known = this.fromNum && this.toNum;\n
      idx = del(o, \'index\');\n
      idxName = del(o, \'name\');\n
      namedIndex = idxName && idxName !== idx;\n
      varPart = "" + idx + " = " + this.fromC;\n
      if (this.toC !== this.toVar) {\n
        varPart += ", " + this.toC;\n
      }\n
      if (this.step !== this.stepVar) {\n
        varPart += ", " + this.step;\n
      }\n
      _ref4 = ["" + idx + " <" + this.equals, "" + idx + " >" + this.equals], lt = _ref4[0], gt = _ref4[1];\n
      condPart = this.stepNum ? +this.stepNum > 0 ? "" + lt + " " + this.toVar : "" + gt + " " + this.toVar : known ? ((_ref5 = [+this.fromNum, +this.toNum], from = _ref5[0], to = _ref5[1], _ref5), from <= to ? "" + lt + " " + to : "" + gt + " " + to) : (cond = this.stepVar ? "" + this.stepVar + " > 0" : "" + this.fromVar + " <= " + this.toVar, "" + cond + " ? " + lt + " " + this.toVar + " : " + gt + " " + this.toVar);\n
      stepPart = this.stepVar ? "" + idx + " += " + this.stepVar : known ? namedIndex ? from <= to ? "++" + idx : "--" + idx : from <= to ? "" + idx + "++" : "" + idx + "--" : namedIndex ? "" + cond + " ? ++" + idx + " : --" + idx : "" + cond + " ? " + idx + "++ : " + idx + "--";\n
      if (namedIndex) {\n
        varPart = "" + idxName + " = " + varPart;\n
      }\n
      if (namedIndex) {\n
        stepPart = "" + idxName + " = " + stepPart;\n
      }\n
      return [this.makeCode("" + varPart + "; " + condPart + "; " + stepPart)];\n
    };\n
\n
    Range.prototype.compileArray = function(o) {\n
      var args, body, cond, hasArgs, i, idt, post, pre, range, result, vars, _i, _ref4, _ref5, _results;\n
      if (this.fromNum && this.toNum && Math.abs(this.fromNum - this.toNum) <= 20) {\n
        range = (function() {\n
          _results = [];\n
          for (var _i = _ref4 = +this.fromNum, _ref5 = +this.toNum; _ref4 <= _ref5 ? _i <= _ref5 : _i >= _ref5; _ref4 <= _ref5 ? _i++ : _i--){ _results.push(_i); }\n
          return _results;\n
        }).apply(this);\n
        if (this.exclusive) {\n
          range.pop();\n
        }\n
        return [this.makeCode("[" + (range.join(\', \')) + "]")];\n
      }\n
      idt = this.tab + TAB;\n
      i = o.scope.freeVariable(\'i\');\n
      result = o.scope.freeVariable(\'results\');\n
      pre = "\\n" + idt + result + " = [];";\n
      if (this.fromNum && this.toNum) {\n
        o.index = i;\n
        body = fragmentsToText(this.compileNode(o));\n
      } else {\n
        vars = ("" + i + " = " + this.fromC) + (this.toC !== this.toVar ? ", " + this.toC : \'\');\n
        cond = "" + this.fromVar + " <= " + this.toVar;\n
        body = "var " + vars + "; " + cond + " ? " + i + " <" + this.equals + " " + this.toVar + " : " + i + " >" + this.equals + " " + this.toVar + "; " + cond + " ? " + i + "++ : " + i + "--";\n
      }\n
      post = "{ " + result + ".push(" + i + "); }\\n" + idt + "return " + result + ";\\n" + o.indent;\n
      hasArgs = function(node) {\n
        return node != null ? node.contains(function(n) {\n
          return n instanceof Literal && n.value === \'arguments\' && !n.asKey;\n
        }) : void 0;\n
      };\n
      if (hasArgs(this.from) || hasArgs(this.to)) {\n
        args = \', arguments\';\n
      }\n
      return [this.makeCode("(function() {" + pre + "\\n" + idt + "for (" + body + ")" + post + "}).apply(this" + (args != null ? args : \'\') + ")")];\n
    };\n
\n
    return Range;\n
\n
  })(Base);\n
\n
  exports.Slice = Slice = (function(_super) {\n
    __extends(Slice, _super);\n
\n
    Slice.prototype.children = [\'range\'];\n
\n
    function Slice(range) {\n
      this.range = range;\n
      Slice.__super__.constructor.call(this);\n
    }\n
\n
    Slice.prototype.compileNode = function(o) {\n
      var compiled, compiledText, from, fromCompiled, to, toStr, _ref4;\n
      _ref4 = this.range, to = _ref4.to, from = _ref4.from;\n
      fromCompiled = from && from.compileToFragments(o, LEVEL_PAREN) || [this.makeCode(\'0\')];\n
      if (to) {\n
        compiled = to.compileToFragments(o, LEVEL_PAREN);\n
        compiledText = fragmentsToText(compiled);\n
        if (!(!this.range.exclusive && +compiledText === -1)) {\n
          toStr = \', \' + (this.range.exclusive ? compiledText : SIMPLENUM.test(compiledText) ? "" + (+compiledText + 1) : (compiled = to.compileToFragments(o, LEVEL_ACCESS), "+" + (fragmentsToText(compiled)) + " + 1 || 9e9"));\n
        }\n
      }\n
      return [this.makeCode(".slice(" + (fragmentsToText(fromCompiled)) + (toStr || \'\') + ")")];\n
    };\n
\n
    return Slice;\n
\n
  })(Base);\n
\n
  exports.Obj = Obj = (function(_super) {\n
    __extends(Obj, _super);\n
\n
    function Obj(props, generated) {\n
      this.generated = generated != null ? generated : false;\n
      this.objects = this.properties = props || [];\n
    }\n
\n
    Obj.prototype.children = [\'properties\'];\n
\n
    Obj.prototype.compileNode = function(o) {\n
      var answer, i, idt, indent, join, lastNoncom, node, prop, props, _i, _j, _len, _len1;\n
      props = this.properties;\n
      if (!props.length) {\n
        return [this.makeCode(this.front ? \'({})\' : \'{}\')];\n
      }\n
      if (this.generated) {\n
        for (_i = 0, _len = props.length; _i < _len; _i++) {\n
          node = props[_i];\n
          if (node instanceof Value) {\n
            node.error(\'cannot have an implicit value in an implicit object\');\n
          }\n
        }\n
      }\n
      idt = o.indent += TAB;\n
      lastNoncom = this.lastNonComment(this.properties);\n
      answer = [];\n
      for (i = _j = 0, _len1 = props.length; _j < _len1; i = ++_j) {\n
        prop = props[i];\n
        join = i === props.length - 1 ? \'\' : prop === lastNoncom || prop instanceof Comment ? \'\\n\' : \',\\

]]></string> </value>
        </item>
        <item>
            <key> <string>next</string> </key>
            <value>
              <persistent> <string encoding="base64">AAAAAAAAAAY=</string> </persistent>
            </value>
        </item>
      </dictionary>
    </pickle>
  </record>
  <record id="6" aka="AAAAAAAAAAY=">
    <pickle>
      <global name="Pdata" module="OFS.Image"/>
    </pickle>
    <pickle>
      <dictionary>
        <item>
            <key> <string>data</string> </key>
            <value> <string encoding="cdata"><![CDATA[

n\';\n
        indent = prop instanceof Comment ? \'\' : idt;\n
        if (prop instanceof Assign && prop.variable instanceof Value && prop.variable.hasProperties()) {\n
          prop.variable.error(\'Invalid object key\');\n
        }\n
        if (prop instanceof Value && prop["this"]) {\n
          prop = new Assign(prop.properties[0].name, prop, \'object\');\n
        }\n
        if (!(prop instanceof Comment)) {\n
          if (!(prop instanceof Assign)) {\n
            prop = new Assign(prop, prop, \'object\');\n
          }\n
          (prop.variable.base || prop.variable).asKey = true;\n
        }\n
        if (indent) {\n
          answer.push(this.makeCode(indent));\n
        }\n
        answer.push.apply(answer, prop.compileToFragments(o, LEVEL_TOP));\n
        if (join) {\n
          answer.push(this.makeCode(join));\n
        }\n
      }\n
      answer.unshift(this.makeCode("{" + (props.length && \'\\n\')));\n
      answer.push(this.makeCode("" + (props.length && \'\\n\' + this.tab) + "}"));\n
      if (this.front) {\n
        return this.wrapInBraces(answer);\n
      } else {\n
        return answer;\n
      }\n
    };\n
\n
    Obj.prototype.assigns = function(name) {\n
      var prop, _i, _len, _ref4;\n
      _ref4 = this.properties;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        prop = _ref4[_i];\n
        if (prop.assigns(name)) {\n
          return true;\n
        }\n
      }\n
      return false;\n
    };\n
\n
    return Obj;\n
\n
  })(Base);\n
\n
  exports.Arr = Arr = (function(_super) {\n
    __extends(Arr, _super);\n
\n
    function Arr(objs) {\n
      this.objects = objs || [];\n
    }\n
\n
    Arr.prototype.children = [\'objects\'];\n
\n
    Arr.prototype.compileNode = function(o) {\n
      var answer, compiledObjs, fragments, index, obj, _i, _len;\n
      if (!this.objects.length) {\n
        return [this.makeCode(\'[]\')];\n
      }\n
      o.indent += TAB;\n
      answer = Splat.compileSplattedArray(o, this.objects);\n
      if (answer.length) {\n
        return answer;\n
      }\n
      answer = [];\n
      compiledObjs = (function() {\n
        var _i, _len, _ref4, _results;\n
        _ref4 = this.objects;\n
        _results = [];\n
        for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
          obj = _ref4[_i];\n
          _results.push(obj.compileToFragments(o, LEVEL_LIST));\n
        }\n
        return _results;\n
      }).call(this);\n
      for (index = _i = 0, _len = compiledObjs.length; _i < _len; index = ++_i) {\n
        fragments = compiledObjs[index];\n
        if (index) {\n
          answer.push(this.makeCode(", "));\n
        }\n
        answer.push.apply(answer, fragments);\n
      }\n
      if (fragmentsToText(answer).indexOf(\'\\n\') >= 0) {\n
        answer.unshift(this.makeCode("[\\n" + o.indent));\n
        answer.push(this.makeCode("\\n" + this.tab + "]"));\n
      } else {\n
        answer.unshift(this.makeCode("["));\n
        answer.push(this.makeCode("]"));\n
      }\n
      return answer;\n
    };\n
\n
    Arr.prototype.assigns = function(name) {\n
      var obj, _i, _len, _ref4;\n
      _ref4 = this.objects;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        obj = _ref4[_i];\n
        if (obj.assigns(name)) {\n
          return true;\n
        }\n
      }\n
      return false;\n
    };\n
\n
    return Arr;\n
\n
  })(Base);\n
\n
  exports.Class = Class = (function(_super) {\n
    __extends(Class, _super);\n
\n
    function Class(variable, parent, body) {\n
      this.variable = variable;\n
      this.parent = parent;\n
      this.body = body != null ? body : new Block;\n
      this.boundFuncs = [];\n
      this.body.classBody = true;\n
    }\n
\n
    Class.prototype.children = [\'variable\', \'parent\', \'body\'];\n
\n
    Class.prototype.determineName = function() {\n
      var decl, tail;\n
      if (!this.variable) {\n
        return null;\n
      }\n
      decl = (tail = last(this.variable.properties)) ? tail instanceof Access && tail.name.value : this.variable.base.value;\n
      if (__indexOf.call(STRICT_PROSCRIBED, decl) >= 0) {\n
        this.variable.error("class variable name may not be " + decl);\n
      }\n
      return decl && (decl = IDENTIFIER.test(decl) && decl);\n
    };\n
\n
    Class.prototype.setContext = function(name) {\n
      return this.body.traverseChildren(false, function(node) {\n
        if (node.classBody) {\n
          return false;\n
        }\n
        if (node instanceof Literal && node.value === \'this\') {\n
          return node.value = name;\n
        } else if (node instanceof Code) {\n
          node.klass = name;\n
          if (node.bound) {\n
            return node.context = name;\n
          }\n
        }\n
      });\n
    };\n
\n
    Class.prototype.addBoundFunctions = function(o) {\n
      var bvar, lhs, _i, _len, _ref4;\n
      _ref4 = this.boundFuncs;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        bvar = _ref4[_i];\n
        lhs = (new Value(new Literal("this"), [new Access(bvar)])).compile(o);\n
        this.ctor.body.unshift(new Literal("" + lhs + " = " + (utility(\'bind\')) + "(" + lhs + ", this)"));\n
      }\n
    };\n
\n
    Class.prototype.addProperties = function(node, name, o) {\n
      var assign, base, exprs, func, props;\n
      props = node.base.properties.slice(0);\n
      exprs = (function() {\n
        var _results;\n
        _results = [];\n
        while (assign = props.shift()) {\n
          if (assign instanceof Assign) {\n
            base = assign.variable.base;\n
            delete assign.context;\n
            func = assign.value;\n
            if (base.value === \'constructor\') {\n
              if (this.ctor) {\n
                assign.error(\'cannot define more than one constructor in a class\');\n
              }\n
              if (func.bound) {\n
                assign.error(\'cannot define a constructor as a bound function\');\n
              }\n
              if (func instanceof Code) {\n
                assign = this.ctor = func;\n
              } else {\n
                this.externalCtor = o.scope.freeVariable(\'class\');\n
                assign = new Assign(new Literal(this.externalCtor), func);\n
              }\n
            } else {\n
              if (assign.variable["this"]) {\n
                func["static"] = true;\n
                if (func.bound) {\n
                  func.context = name;\n
                }\n
              } else {\n
                assign.variable = new Value(new Literal(name), [new Access(new Literal(\'prototype\')), new Access(base)]);\n
                if (func instanceof Code && func.bound) {\n
                  this.boundFuncs.push(base);\n
                  func.bound = false;\n
                }\n
              }\n
            }\n
          }\n
          _results.push(assign);\n
        }\n
        return _results;\n
      }).call(this);\n
      return compact(exprs);\n
    };\n
\n
    Class.prototype.walkBody = function(name, o) {\n
      var _this = this;\n
      return this.traverseChildren(false, function(child) {\n
        var cont, exps, i, node, _i, _len, _ref4;\n
        cont = true;\n
        if (child instanceof Class) {\n
          return false;\n
        }\n
        if (child instanceof Block) {\n
          _ref4 = exps = child.expressions;\n
          for (i = _i = 0, _len = _ref4.length; _i < _len; i = ++_i) {\n
            node = _ref4[i];\n
            if (node instanceof Value && node.isObject(true)) {\n
              cont = false;\n
              exps[i] = _this.addProperties(node, name, o);\n
            }\n
          }\n
          child.expressions = exps = flatten(exps);\n
        }\n
        return cont && !(child instanceof Class);\n
      });\n
    };\n
\n
    Class.prototype.hoistDirectivePrologue = function() {\n
      var expressions, index, node;\n
      index = 0;\n
      expressions = this.body.expressions;\n
      while ((node = expressions[index]) && node instanceof Comment || node instanceof Value && node.isString()) {\n
        ++index;\n
      }\n
      return this.directives = expressions.splice(0, index);\n
    };\n
\n
    Class.prototype.ensureConstructor = function(name, o) {\n
      var missing, ref, superCall;\n
      missing = !this.ctor;\n
      this.ctor || (this.ctor = new Code);\n
      this.ctor.ctor = this.ctor.name = name;\n
      this.ctor.klass = null;\n
      this.ctor.noReturn = true;\n
      if (missing) {\n
        if (this.parent) {\n
          superCall = new Literal("" + name + ".__super__.constructor.apply(this, arguments)");\n
        }\n
        if (this.externalCtor) {\n
          superCall = new Literal("" + this.externalCtor + ".apply(this, arguments)");\n
        }\n
        if (superCall) {\n
          ref = new Literal(o.scope.freeVariable(\'ref\'));\n
          this.ctor.body.unshift(new Assign(ref, superCall));\n
        }\n
        this.addBoundFunctions(o);\n
        if (superCall) {\n
          this.ctor.body.push(ref);\n
          this.ctor.body.makeReturn();\n
        }\n
        return this.body.expressions.unshift(this.ctor);\n
      } else {\n
        return this.addBoundFunctions(o);\n
      }\n
    };\n
\n
    Class.prototype.compileNode = function(o) {\n
      var call, decl, klass, lname, name, params, _ref4;\n
      decl = this.determineName();\n
      name = decl || \'_Class\';\n
      if (name.reserved) {\n
        name = "_" + name;\n
      }\n
      lname = new Literal(name);\n
      this.hoistDirectivePrologue();\n
      this.setContext(name);\n
      this.walkBody(name, o);\n
      this.ensureConstructor(name, o);\n
      this.body.spaced = true;\n
      if (!(this.ctor instanceof Code)) {\n
        this.body.expressions.unshift(this.ctor);\n
      }\n
      this.body.expressions.push(lname);\n
      (_ref4 = this.body.expressions).unshift.apply(_ref4, this.directives);\n
      call = Closure.wrap(this.body);\n
      if (this.parent) {\n
        this.superClass = new Literal(o.scope.freeVariable(\'super\', false));\n
        this.body.expressions.unshift(new Extends(lname, this.superClass));\n
        call.args.push(this.parent);\n
        params = call.variable.params || call.variable.base.params;\n
        params.push(new Param(this.superClass));\n
      }\n
      klass = new Parens(call, true);\n
      if (this.variable) {\n
        klass = new Assign(this.variable, klass);\n
      }\n
      return klass.compileToFragments(o);\n
    };\n
\n
    return Class;\n
\n
  })(Base);\n
\n
  exports.Assign = Assign = (function(_super) {\n
    __extends(Assign, _super);\n
\n
    function Assign(variable, value, context, options) {\n
      var forbidden, name, _ref4;\n
      this.variable = variable;\n
      this.value = value;\n
      this.context = context;\n
      this.param = options && options.param;\n
      this.subpattern = options && options.subpattern;\n
      forbidden = (_ref4 = (name = this.variable.unwrapAll().value), __indexOf.call(STRICT_PROSCRIBED, _ref4) >= 0);\n
      if (forbidden && this.context !== \'object\') {\n
        this.variable.error("variable name may not be \\"" + name + "\\"");\n
      }\n
    }\n
\n
    Assign.prototype.children = [\'variable\', \'value\'];\n
\n
    Assign.prototype.isStatement = function(o) {\n
      return (o != null ? o.level : void 0) === LEVEL_TOP && (this.context != null) && __indexOf.call(this.context, "?") >= 0;\n
    };\n
\n
    Assign.prototype.assigns = function(name) {\n
      return this[this.context === \'object\' ? \'value\' : \'variable\'].assigns(name);\n
    };\n
\n
    Assign.prototype.unfoldSoak = function(o) {\n
      return unfoldSoak(o, this, \'variable\');\n
    };\n
\n
    Assign.prototype.compileNode = function(o) {\n
      var answer, compiledName, isValue, match, name, val, varBase, _ref4, _ref5, _ref6, _ref7;\n
      if (isValue = this.variable instanceof Value) {\n
        if (this.variable.isArray() || this.variable.isObject()) {\n
          return this.compilePatternMatch(o);\n
        }\n
        if (this.variable.isSplice()) {\n
          return this.compileSplice(o);\n
        }\n
        if ((_ref4 = this.context) === \'||=\' || _ref4 === \'&&=\' || _ref4 === \'?=\') {\n
          return this.compileConditional(o);\n
        }\n
      }\n
      compiledName = this.variable.compileToFragments(o, LEVEL_LIST);\n
      name = fragmentsToText(compiledName);\n
      if (!this.context) {\n
        varBase = this.variable.unwrapAll();\n
        if (!varBase.isAssignable()) {\n
          this.variable.error("\\"" + (this.variable.compile(o)) + "\\" cannot be assigned");\n
        }\n
        if (!(typeof varBase.hasProperties === "function" ? varBase.hasProperties() : void 0)) {\n
          if (this.param) {\n
            o.scope.add(name, \'var\');\n
          } else {\n
            o.scope.find(name);\n
          }\n
        }\n
      }\n
      if (this.value instanceof Code && (match = METHOD_DEF.exec(name))) {\n
        if (match[1]) {\n
          this.value.klass = match[1];\n
        }\n
        this.value.name = (_ref5 = (_ref6 = (_ref7 = match[2]) != null ? _ref7 : match[3]) != null ? _ref6 : match[4]) != null ? _ref5 : match[5];\n
      }\n
      val = this.value.compileToFragments(o, LEVEL_LIST);\n
      if (this.context === \'object\') {\n
        return compiledName.concat(this.makeCode(": "), val);\n
      }\n
      answer = compiledName.concat(this.makeCode(" " + (this.context || \'=\') + " "), val);\n
      if (o.level <= LEVEL_LIST) {\n
        return answer;\n
      } else {\n
        return this.wrapInBraces(answer);\n
      }\n
    };\n
\n
    Assign.prototype.compilePatternMatch = function(o) {\n
      var acc, assigns, code, fragments, i, idx, isObject, ivar, name, obj, objects, olen, ref, rest, splat, top, val, value, vvar, vvarText, _i, _len, _ref4, _ref5, _ref6, _ref7, _ref8, _ref9;\n
      top = o.level === LEVEL_TOP;\n
      value = this.value;\n
      objects = this.variable.base.objects;\n
      if (!(olen = objects.length)) {\n
        code = value.compileToFragments(o);\n
        if (o.level >= LEVEL_OP) {\n
          return this.wrapInBraces(code);\n
        } else {\n
          return code;\n
        }\n
      }\n
      isObject = this.variable.isObject();\n
      if (top && olen === 1 && !((obj = objects[0]) instanceof Splat)) {\n
        if (obj instanceof Assign) {\n
          _ref4 = obj, (_ref5 = _ref4.variable, idx = _ref5.base), obj = _ref4.value;\n
        } else {\n
          idx = isObject ? obj["this"] ? obj.properties[0].name : obj : new Literal(0);\n
        }\n
        acc = IDENTIFIER.test(idx.unwrap().value || 0);\n
        value = new Value(value);\n
        value.properties.push(new (acc ? Access : Index)(idx));\n
        if (_ref6 = obj.unwrap().value, __indexOf.call(RESERVED, _ref6) >= 0) {\n
          obj.error("assignment to a reserved word: " + (obj.compile(o)));\n
        }\n
        return new Assign(obj, value, null, {\n
          param: this.param\n
        }).compileToFragments(o, LEVEL_TOP);\n
      }\n
      vvar = value.compileToFragments(o, LEVEL_LIST);\n
      vvarText = fragmentsToText(vvar);\n
      assigns = [];\n
      splat = false;\n
      if (!IDENTIFIER.test(vvarText) || this.variable.assigns(vvarText)) {\n
        assigns.push([this.makeCode("" + (ref = o.scope.freeVariable(\'ref\')) + " = ")].concat(__slice.call(vvar)));\n
        vvar = [this.makeCode(ref)];\n
        vvarText = ref;\n
      }\n
      for (i = _i = 0, _len = objects.length; _i < _len; i = ++_i) {\n
        obj = objects[i];\n
        idx = i;\n
        if (isObject) {\n
          if (obj instanceof Assign) {\n
            _ref7 = obj, (_ref8 = _ref7.variable, idx = _ref8.base), obj = _ref7.value;\n
          } else {\n
            if (obj.base instanceof Parens) {\n
              _ref9 = new Value(obj.unwrapAll()).cacheReference(o), obj = _ref9[0], idx = _ref9[1];\n
            } else {\n
              idx = obj["this"] ? obj.properties[0].name : obj;\n
            }\n
          }\n
        }\n
        if (!splat && obj instanceof Splat) {\n
          name = obj.name.unwrap().value;\n
          obj = obj.unwrap();\n
          val = "" + olen + " <= " + vvarText + ".length ? " + (utility(\'slice\')) + ".call(" + vvarText + ", " + i;\n
          if (rest = olen - i - 1) {\n
            ivar = o.scope.freeVariable(\'i\');\n
            val += ", " + ivar + " = " + vvarText + ".length - " + rest + ") : (" + ivar + " = " + i + ", [])";\n
          } else {\n
            val += ") : []";\n
          }\n
          val = new Literal(val);\n
          splat = "" + ivar + "++";\n
        } else {\n
          name = obj.unwrap().value;\n
          if (obj instanceof Splat) {\n
            obj.error("multiple splats are disallowed in an assignment");\n
          }\n
          if (typeof idx === \'number\') {\n
            idx = new Literal(splat || idx);\n
            acc = false;\n
          } else {\n
            acc = isObject && IDENTIFIER.test(idx.unwrap().value || 0);\n
          }\n
          val = new Value(new Literal(vvarText), [new (acc ? Access : Index)(idx)]);\n
        }\n
        if ((name != null) && __indexOf.call(RESERVED, name) >= 0) {\n
          obj.error("assignment to a reserved word: " + (obj.compile(o)));\n
        }\n
        assigns.push(new Assign(obj, val, null, {\n
          param: this.param,\n
          subpattern: true\n
        }).compileToFragments(o, LEVEL_LIST));\n
      }\n
      if (!(top || this.subpattern)) {\n
        assigns.push(vvar);\n
      }\n
      fragments = this.joinFragmentArrays(assigns, \', \');\n
      if (o.level < LEVEL_LIST) {\n
        return fragments;\n
      } else {\n
        return this.wrapInBraces(fragments);\n
      }\n
    };\n
\n
    Assign.prototype.compileConditional = function(o) {\n
      var left, right, _ref4;\n
      _ref4 = this.variable.cacheReference(o), left = _ref4[0], right = _ref4[1];\n
      if (!left.properties.length && left.base instanceof Literal && left.base.value !== "this" && !o.scope.check(left.base.value)) {\n
        this.variable.error("the variable \\"" + left.base.value + "\\" can\'t be assigned with " + this.context + " because it has not been declared before");\n
      }\n
      if (__indexOf.call(this.context, "?") >= 0) {\n
        o.isExistentialEquals = true;\n
      }\n
      return new Op(this.context.slice(0, -1), left, new Assign(right, this.value, \'=\')).compileToFragments(o);\n
    };\n
\n
    Assign.prototype.compileSplice = function(o) {\n
      var answer, exclusive, from, fromDecl, fromRef, name, to, valDef, valRef, _ref4, _ref5, _ref6;\n
      _ref4 = this.variable.properties.pop().range, from = _ref4.from, to = _ref4.to, exclusive = _ref4.exclusive;\n
      name = this.variable.compile(o);\n
      if (from) {\n
        _ref5 = this.cacheToCodeFragments(from.cache(o, LEVEL_OP)), fromDecl = _ref5[0], fromRef = _ref5[1];\n
      } else {\n
        fromDecl = fromRef = \'0\';\n
      }\n
      if (to) {\n
        if ((from != null ? from.isSimpleNumber() : void 0) && to.isSimpleNumber()) {\n
          to = +to.compile(o) - +fromRef;\n
          if (!exclusive) {\n
            to += 1;\n
          }\n
        } else {\n
          to = to.compile(o, LEVEL_ACCESS) + \' - \' + fromRef;\n
          if (!exclusive) {\n
            to += \' + 1\';\n
          }\n
        }\n
      } else {\n
        to = "9e9";\n
      }\n
      _ref6 = this.value.cache(o, LEVEL_LIST), valDef = _ref6[0], valRef = _ref6[1];\n
      answer = [].concat(this.makeCode("[].splice.apply(" + name + ", [" + fromDecl + ", " + to + "].concat("), valDef, this.makeCode(")), "), valRef);\n
      if (o.level > LEVEL_TOP) {\n
        return this.wrapInBraces(answer);\n
      } else {\n
        return answer;\n
      }\n
    };\n
\n
    return Assign;\n
\n
  })(Base);\n
\n
  exports.Code = Code = (function(_super) {\n
    __extends(Code, _super);\n
\n
    function Code(params, body, tag) {\n
      this.params = params || [];\n
      this.body = body || new Block;\n
      this.bound = tag === \'boundfunc\';\n
      if (this.bound) {\n
        this.context = \'_this\';\n
      }\n
    }\n
\n
    Code.prototype.children = [\'params\', \'body\'];\n
\n
    Code.prototype.isStatement = function() {\n
      return !!this.ctor;\n
    };\n
\n
    Code.prototype.jumps = NO;\n
\n
    Code.prototype.compileNode = function(o) {\n
      var answer, code, exprs, i, idt, lit, p, param, params, ref, splats, uniqs, val, wasEmpty, _i, _j, _k, _l, _len, _len1, _len2, _len3, _len4, _m, _ref4, _ref5, _ref6, _ref7, _ref8;\n
      o.scope = new Scope(o.scope, this.body, this);\n
      o.scope.shared = del(o, \'sharedScope\');\n
      o.indent += TAB;\n
      delete o.bare;\n
      delete o.isExistentialEquals;\n
      params = [];\n
      exprs = [];\n
      this.eachParamName(function(name) {\n
        if (!o.scope.check(name)) {\n
          return o.scope.parameter(name);\n
        }\n
      });\n
      _ref4 = this.params;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        param = _ref4[_i];\n
        if (!param.splat) {\n
          continue;\n
        }\n
        _ref5 = this.params;\n
        for (_j = 0, _len1 = _ref5.length; _j < _len1; _j++) {\n
          p = _ref5[_j].name;\n
          if (p["this"]) {\n
            p = p.properties[0].name;\n
          }\n
          if (p.value) {\n
            o.scope.add(p.value, \'var\', true);\n
          }\n
        }\n
        splats = new Assign(new Value(new Arr((function() {\n
          var _k, _len2, _ref6, _results;\n
          _ref6 = this.params;\n
          _results = [];\n
          for (_k = 0, _len2 = _ref6.length; _k < _len2; _k++) {\n
            p = _ref6[_k];\n
            _results.push(p.asReference(o));\n
          }\n
          return _results;\n
        }).call(this))), new Value(new Literal(\'arguments\')));\n
        break;\n
      }\n
      _ref6 = this.params;\n
      for (_k = 0, _len2 = _ref6.length; _k < _len2; _k++) {\n
        param = _ref6[_k];\n
        if (param.isComplex()) {\n
          val = ref = param.asReference(o);\n
          if (param.value) {\n
            val = new Op(\'?\', ref, param.value);\n
          }\n
          exprs.push(new Assign(new Value(param.name), val, \'=\', {\n
            param: true\n
          }));\n
        } else {\n
          ref = param;\n
          if (param.value) {\n
            lit = new Literal(ref.name.value + \' == null\');\n
            val = new Assign(new Value(param.name), param.value, \'=\');\n
            exprs.push(new If(lit, val));\n
          }\n
        }\n
        if (!splats) {\n
          params.push(ref);\n
        }\n
      }\n
      wasEmpty = this.body.isEmpty();\n
      if (splats) {\n
        exprs.unshift(splats);\n
      }\n
      if (exprs.length) {\n
        (_ref7 = this.body.expressions).unshift.apply(_ref7, exprs);\n
      }\n
      for (i = _l = 0, _len3 = params.length; _l < _len3; i = ++_l) {\n
        p = params[i];\n
        params[i] = p.compileToFragments(o);\n
        o.scope.parameter(fragmentsToText(params[i]));\n
      }\n
      uniqs = [];\n
      this.eachParamName(function(name, node) {\n
        if (__indexOf.call(uniqs, name) >= 0) {\n
          node.error("multiple parameters named \'" + name + "\'");\n
        }\n
        return uniqs.push(name);\n
      });\n
      if (!(wasEmpty || this.noReturn)) {\n
        this.body.makeReturn();\n
      }\n
      if (this.bound) {\n
        if ((_ref8 = o.scope.parent.method) != null ? _ref8.bound : void 0) {\n
          this.bound = this.context = o.scope.parent.method.context;\n
        } else if (!this["static"]) {\n
          o.scope.parent.assign(\'_this\', \'this\');\n
        }\n
      }\n
      idt = o.indent;\n
      code = \'function\';\n
      if (this.ctor) {\n
        code += \' \' + this.name;\n
      }\n
      code += \'(\';\n
      answer = [this.makeCode(code)];\n
      for (i = _m = 0, _len4 = params.length; _m < _len4; i = ++_m) {\n
        p = params[i];\n
        if (i) {\n
          answer.push(this.makeCode(", "));\n
        }\n
        answer.push.apply(answer, p);\n
      }\n
      answer.push(this.makeCode(\') {\'));\n
      if (!this.body.isEmpty()) {\n
        answer = answer.concat(this.makeCode("\\n"), this.body.compileWithDeclarations(o), this.makeCode("\\n" + this.tab));\n
      }\n
      answer.push(this.makeCode(\'}\'));\n
      if (this.ctor) {\n
        return [this.makeCode(this.tab)].concat(__slice.call(answer));\n
      }\n
      if (this.front || (o.level >= LEVEL_ACCESS)) {\n
        return this.wrapInBraces(answer);\n
      } else {\n
        return answer;\n
      }\n
    };\n
\n
    Code.prototype.eachParamName = function(iterator) {\n
      var param, _i, _len, _ref4, _results;\n
      _ref4 = this.params;\n
      _results = [];\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        param = _ref4[_i];\n
        _results.push(param.eachName(iterator));\n
      }\n
      return _results;\n
    };\n
\n
    Code.prototype.traverseChildren = function(crossScope, func) {\n
      if (crossScope) {\n
        return Code.__super__.traverseChildren.call(this, crossScope, func);\n
      }\n
    };\n
\n
    return Code;\n
\n
  })(Base);\n
\n
  exports.Param = Param = (function(_super) {\n
    __extends(Param, _super);\n
\n
    function Param(name, value, splat) {\n
      var _ref4;\n
      this.name = name;\n
      this.value = value;\n
      this.splat = splat;\n
      if (_ref4 = (name = this.name.unwrapAll().value), __indexOf.call(STRICT_PROSCRIBED, _ref4) >= 0) {\n
        this.name.error("parameter name \\"" + name + "\\" is not allowed");\n
      }\n
    }\n
\n
    Param.prototype.children = [\'name\', \'value\'];\n
\n
    Param.prototype.compileToFragments = function(o) {\n
      return this.name.compileToFragments(o, LEVEL_LIST);\n
    };\n
\n
    Param.prototype.asReference = function(o) {\n
      var node;\n
      if (this.reference) {\n
        return this.reference;\n
      }\n
      node = this.name;\n
      if (node["this"]) {\n
        node = node.properties[0].name;\n
        if (node.value.reserved) {\n
          node = new Literal(o.scope.freeVariable(node.value));\n
        }\n
      } else if (node.isComplex()) {\n
        node = new Literal(o.scope.freeVariable(\'arg\'));\n
      }\n
      node = new Value(node);\n
      if (this.splat) {\n
        node = new Splat(node);\n
      }\n
      return this.reference = node;\n
    };\n
\n
    Param.prototype.isComplex = function() {\n
      return this.name.isComplex();\n
    };\n
\n
    Param.prototype.eachName = function(iterator, name) {\n
      var atParam, node, obj, _i, _len, _ref4;\n
      if (name == null) {\n
        name = this.name;\n
      }\n
      atParam = function(obj) {\n
        var node;\n
        node = obj.properties[0].name;\n
        if (!node.value.reserved) {\n
          return iterator(node.value, node);\n
        }\n
      };\n
      if (name instanceof Literal) {\n
        return iterator(name.value, name);\n
      }\n
      if (name instanceof Value) {\n
        return atParam(name);\n
      }\n
      _ref4 = name.objects;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        obj = _ref4[_i];\n
        if (obj instanceof Assign) {\n
          this.eachName(iterator, obj.value.unwrap());\n
        } else if (obj instanceof Splat) {\n
          node = obj.name.unwrap();\n
          iterator(node.value, node);\n
        } else if (obj instanceof Value) {\n
          if (obj.isArray() || obj.isObject()) {\n
            this.eachName(iterator, obj.base);\n
          } else if (obj["this"]) {\n
            atParam(obj);\n
          } else {\n
            iterator(obj.base.value, obj.base);\n
          }\n
        } else {\n
          obj.error("illegal parameter " + (obj.compile()));\n
        }\n
      }\n
    };\n
\n
    return Param;\n
\n
  })(Base);\n
\n
  exports.Splat = Splat = (function(_super) {\n
    __extends(Splat, _super);\n
\n
    Splat.prototype.children = [\'name\'];\n
\n
    Splat.prototype.isAssignable = YES;\n
\n
    function Splat(name) {\n
      this.name = name.compile ? name : new Literal(name);\n
    }\n
\n
    Splat.prototype.assigns = function(name) {\n
      return this.name.assigns(name);\n
    };\n
\n
    Splat.prototype.compileToFragments = function(o) {\n
      return this.name.compileToFragments(o);\n
    };\n
\n
    Splat.prototype.unwrap = function() {\n
      return this.name;\n
    };\n
\n
    Splat.compileSplattedArray = function(o, list, apply) {\n
      var args, base, compiledNode, concatPart, fragments, i, index, node, _i, _len;\n
      index = -1;\n
      while ((node = list[++index]) && !(node instanceof Splat)) {\n
        continue;\n
      }\n
      if (index >= list.length) {\n
        return [];\n
      }\n
      if (list.length === 1) {\n
        node = list[0];\n
        fragments = node.compileToFragments(o, LEVEL_LIST);\n
        if (apply) {\n
          return fragments;\n
        }\n
        return [].concat(node.makeCode("" + (utility(\'slice\')) + ".call("), fragments, node.makeCode(")"));\n
      }\n
      args = list.slice(index);\n
      for (i = _i = 0, _len = args.length; _i < _len; i = ++_i) {\n
        node = args[i];\n
        compiledNode = node.compileToFragments(o, LEVEL_LIST);\n
        args[i] = node instanceof Splat ? [].concat(node.makeCode("" + (utility(\'slice\')) + ".call("), compiledNode, node.makeCode(")")) : [].concat(node.makeCode("["), compiledNode, node.makeCode("]"));\n
      }\n
      if (index === 0) {\n
        node = list[0];\n
        concatPart = node.joinFragmentArrays(args.slice(1), \', \');\n
        return args[0].concat(node.makeCode(".concat("), concatPart, node.makeCode(")"));\n
      }\n
      base = (function() {\n
        var _j, _len1, _ref4, _results;\n
        _ref4 = list.slice(0, index);\n
        _results = [];\n
        for (_j = 0, _len1 = _ref4.length; _j < _len1; _j++) {\n
          node = _ref4[_j];\n
          _results.push(node.compileToFragments(o, LEVEL_LIST));\n
        }\n
        return _results;\n
      })();\n
      base = list[0].joinFragmentArrays(base, \', \');\n
      concatPart = list[index].joinFragmentArrays(args, \', \');\n
      return [].concat(list[0].makeCode("["), base, list[index].makeCode("].concat("), concatPart, (last(list)).makeCode(")"));\n
    };\n
\n
    return Splat;\n
\n
  })(Base);\n
\n
  exports.While = While = (function(_super) {\n
    __extends(While, _super);\n
\n
    function While(condition, options) {\n
      this.condition = (options != null ? options.invert : void 0) ? condition.invert() : condition;\n
      this.guard = options != null ? options.guard : void 0;\n
    }\n
\n
    While.prototype.children = [\'condition\', \'guard\', \'body\'];\n
\n
    While.prototype.isStatement = YES;\n
\n
    While.prototype.makeReturn = function(res) {\n
      if (res) {\n
        return While.__super__.makeReturn.apply(this, arguments);\n
      } else {\n
        this.returns = !this.jumps({\n
          loop: true\n
        });\n
        return this;\n
      }\n
    };\n
\n
    While.prototype.addBody = function(body) {\n
      this.body = body;\n
      return this;\n
    };\n
\n
    While.prototype.jumps = function() {\n
      var expressions, node, _i, _len;\n
      expressions = this.body.expressions;\n
      if (!expressions.length) {\n
        return false;\n
      }\n
      for (_i = 0, _len = expressions.length; _i < _len; _i++) {\n
        node = expressions[_i];\n
        if (node.jumps({\n
          loop: true\n
        })) {\n
          return node;\n
        }\n
      }\n
      return false;\n
    };\n
\n
    While.prototype.compileNode = function(o) {\n
      var answer, body, rvar, set;\n
      o.indent += TAB;\n
      set = \'\';\n
      body = this.body;\n
      if (body.isEmpty()) {\n
        body = this.makeCode(\'\');\n
      } else {\n
        if (this.returns) {\n
          body.makeReturn(rvar = o.scope.freeVariable(\'results\'));\n
          set = "" + this.tab + rvar + " = [];\\n";\n
        }\n
        if (this.guard) {\n
          if (body.expressions.length > 1) {\n
            body.expressions.unshift(new If((new Parens(this.guard)).invert(), new Literal("continue")));\n
          } else {\n
            if (this.guard) {\n
              body = Block.wrap([new If(this.guard, body)]);\n
            }\n
          }\n
        }\n
        body = [].concat(this.makeCode("\\n"), body.compileToFragments(o, LEVEL_TOP), this.makeCode("\\n" + this.tab));\n
      }\n
      answer = [].concat(this.makeCode(set + this.tab + "while ("), this.condition.compileToFragments(o, LEVEL_PAREN), this.makeCode(") {"), body, this.makeCode("}"));\n
      if (this.returns) {\n
        answer.push(this.makeCode("\\n" + this.tab + "return " + rvar + ";"));\n
      }\n
      return answer;\n
    };\n
\n
    return While;\n
\n
  })(Base);\n
\n
  exports.Op = Op = (function(_super) {\n
    var CONVERSIONS, INVERSIONS;\n
\n
    __extends(Op, _super);\n
\n
    function Op(op, first, second, flip) {\n
      if (op === \'in\') {\n
        return new In(first, second);\n
      }\n
      if (op === \'do\') {\n
        return this.generateDo(first);\n
      }\n
      if (op === \'new\') {\n
        if (first instanceof Call && !first["do"] && !first.isNew) {\n
          return first.newInstance();\n
        }\n
        if (first instanceof Code && first.bound || first["do"]) {\n
          first = new Parens(first);\n
        }\n
      }\n
      this.operator = CONVERSIONS[op] || op;\n
      this.first = first;\n
      this.second = second;\n
      this.flip = !!flip;\n
      return this;\n
    }\n
\n
    CONVERSIONS = {\n
      \'==\': \'===\',\n
      \'!=\': \'!==\',\n
      \'of\': \'in\'\n
    };\n
\n
    INVERSIONS = {\n
      \'!==\': \'===\',\n
      \'===\': \'!==\'\n
    };\n
\n
    Op.prototype.children = [\'first\', \'second\'];\n
\n
    Op.prototype.isSimpleNumber = NO;\n
\n
    Op.prototype.isUnary = function() {\n
      return !this.second;\n
    };\n
\n
    Op.prototype.isComplex = function() {\n
      var _ref4;\n
      return !(this.isUnary() && ((_ref4 = this.operator) === \'+\' || _ref4 === \'-\')) || this.first.isComplex();\n
    };\n
\n
    Op.prototype.isChainable = function() {\n
      var _ref4;\n
      return (_ref4 = this.operator) === \'<\' || _ref4 === \'>\' || _ref4 === \'>=\' || _ref4 === \'<=\' || _ref4 === \'===\' || _ref4 === \'!==\';\n
    };\n
\n
    Op.prototype.invert = function() {\n
      var allInvertable, curr, fst, op, _ref4;\n
      if (this.isChainable() && this.first.isChainable()) {\n
        allInvertable = true;\n
        curr = this;\n
        while (curr && curr.operator) {\n
          allInvertable && (allInvertable = curr.operator in INVERSIONS);\n
          curr = curr.first;\n
        }\n
        if (!allInvertable) {\n
          return new Parens(this).invert();\n
        }\n
        curr = this;\n
        while (curr && curr.operator) {\n
          curr.invert = !curr.invert;\n
          curr.operator = INVERSIONS[curr.operator];\n
          curr = curr.first;\n
        }\n
        return this;\n
      } else if (op = INVERSIONS[this.operator]) {\n
        this.operator = op;\n
        if (this.first.unwrap() instanceof Op) {\n
          this.first.invert();\n
        }\n
        return this;\n
      } else if (this.second) {\n
        return new Parens(this).invert();\n
      } else if (this.operator === \'!\' && (fst = this.first.unwrap()) instanceof Op && ((_ref4 = fst.operator) === \'!\' || _ref4 === \'in\' || _ref4 === \'instanceof\')) {\n
        return fst;\n
      } else {\n
        return new Op(\'!\', this);\n
      }\n
    };\n
\n
    Op.prototype.unfoldSoak = function(o) {\n
      var _ref4;\n
      return ((_ref4 = this.operator) === \'++\' || _ref4 === \'--\' || _ref4 === \'delete\') && unfoldSoak(o, this, \'first\');\n
    };\n
\n
    Op.prototype.generateDo = function(exp) {\n
      var call, func, param, passedParams, ref, _i, _len, _ref4;\n
      passedParams = [];\n
      func = exp instanceof Assign && (ref = exp.value.unwrap()) instanceof Code ? ref : exp;\n
      _ref4 = func.params || [];\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        param = _ref4[_i];\n
        if (param.value) {\n
          passedParams.push(param.value);\n
          delete param.value;\n
        } else {\n
          passedParams.push(param);\n
        }\n
      }\n
      call = new Call(exp, passedParams);\n
      call["do"] = true;\n
      return call;\n
    };\n
\n
    Op.prototype.compileNode = function(o) {\n
      var answer, isChain, _ref4, _ref5;\n
      isChain = this.isChainable() && this.first.isChainable();\n
      if (!isChain) {\n
        this.first.front = this.front;\n
      }\n
      if (this.operator === \'delete\' && o.scope.check(this.first.unwrapAll().value)) {\n
        this.error(\'delete operand may not be argument or var\');\n
      }\n
      if (((_ref4 = this.operator) === \'--\' || _ref4 === \'++\') && (_ref5 = this.first.unwrapAll().value, __indexOf.call(STRICT_PROSCRIBED, _ref5) >= 0)) {\n
        this.error("cannot increment/decrement \\"" + (this.first.unwrapAll().value) + "\\"");\n
      }\n
      if (this.isUnary()) {\n
        return this.compileUnary(o);\n
      }\n
      if (isChain) {\n
        return this.compileChain(o);\n
      }\n
      if (this.operator === \'?\') {\n
        return this.compileExistence(o);\n
      }\n
      answer = [].concat(this.first.compileToFragments(o, LEVEL_OP), this.makeCode(\' \' + this.operator + \' \'), this.second.compileToFragments(o, LEVEL_OP));\n
      if (o.level <= LEVEL_OP) {\n
        return answer;\n
      } else {\n
        return this.wrapInBraces(answer);\n
      }\n
    };\n
\n
    Op.prototype.compileChain = function(o) {\n
      var fragments, fst, shared, _ref4;\n
      _ref4 = this.first.second.cache(o), this.first.second = _ref4[0], shared = _ref4[1];\n
      fst = this.first.compileToFragments(o, LEVEL_OP);\n
      fragments = fst.concat(this.makeCode(" " + (this.invert ? \'&&\' : \'||\') + " "), shared.compileToFragments(o), this.makeCode(" " + this.operator + " "), this.second.compileToFragments(o, LEVEL_OP));\n
      return this.wrapInBraces(fragments);\n
    };\n
\n
    Op.prototype.compileExistence = function(o) {\n
      var fst, ref;\n
      if (!o.isExistentialEquals && this.first.isComplex()) {\n
        ref = new Literal(o.scope.freeVariable(\'ref\'));\n
        fst = new Parens(new Assign(ref, this.first));\n
      } else {\n
        fst = this.first;\n
        ref = fst;\n
      }\n
      return new If(new Existence(fst), ref, {\n
        type: \'if\'\n
      }).addElse(this.second).compileToFragments(o);\n
    };\n
\n
    Op.prototype.compileUnary = function(o) {\n
      var op, parts, plusMinus;\n
      parts = [];\n
      op = this.operator;\n
      parts.push([this.makeCode(op)]);\n
      if (op === \'!\' && this.first instanceof Existence) {\n
        this.first.negated = !this.first.negated;\n
        return this.first.compileToFragments(o);\n
      }\n
      if (o.level >= LEVEL_ACCESS) {\n
        return (new Parens(this)).compileToFragments(o);\n
      }\n
      plusMinus = op === \'+\' || op === \'-\';\n
      if ((op === \'new\' || op === \'typeof\' || op === \'delete\') || plusMinus && this.first instanceof Op && this.first.operator === op) {\n
        parts.push([this.makeCode(\' \')]);\n
      }\n
      if ((plusMinus && this.first instanceof Op) || (op === \'new\' && this.first.isStatement(o))) {\n
        this.first = new Parens(this.first);\n
      }\n
      parts.push(this.first.compileToFragments(o, LEVEL_OP));\n
      if (this.flip) {\n
        parts.reverse();\n
      }\n
      return this.joinFragmentArrays(parts, \'\');\n
    };\n
\n
    Op.prototype.toString = function(idt) {\n
      return Op.__super__.toString.call(this, idt, this.constructor.name + \' \' + this.operator);\n
    };\n
\n
    return Op;\n
\n
  })(Base);\n
\n
  exports.In = In = (function(_super) {\n
    __extends(In, _super);\n
\n
    function In(object, array) {\n
      this.object = object;\n
      this.array = array;\n
    }\n
\n
    In.prototype.children = [\'object\', \'array\'];\n
\n
    In.prototype.invert = NEGATE;\n
\n
    In.prototype.compileNode = function(o) {\n
      var hasSplat, obj, _i, _len, _ref4;\n
      if (this.array instanceof Value && this.array.isArray()) {\n
        _ref4 = this.array.base.objects;\n
        for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
          obj = _ref4[_i];\n
          if (!(obj instanceof Splat)) {\n
            continue;\n
          }\n
          hasSplat = true;\n
          break;\n
        }\n
        if (!hasSplat) {\n
          return this.compileOrTest(o);\n
        }\n
      }\n
      return this.compileLoopTest(o);\n
    };\n
\n
    In.prototype.compileOrTest = function(o) {\n
      var cmp, cnj, i, item, ref, sub, tests, _i, _len, _ref4, _ref5, _ref6;\n
      if (this.array.base.objects.length === 0) {\n
        return [this.makeCode("" + (!!this.negated))];\n
      }\n
      _ref4 = this.object.cache(o, LEVEL_OP), sub = _ref4[0], ref = _ref4[1];\n
      _ref5 = this.negated ? [\' !== \', \' && \'] : [\' === \', \' || \'], cmp = _ref5[0], cnj = _ref5[1];\n
      tests = [];\n
      _ref6 = this.array.base.objects;\n
      for (i = _i = 0, _len = _ref6.length; _i < _len; i = ++_i) {\n
        item = _ref6[i];\n
        if (i) {\n
          tests.push(this.makeCode(cnj));\n
        }\n
        tests = tests.concat((i ? ref : sub), this.makeCode(cmp), item.compileToFragments(o, LEVEL_ACCESS));\n
      }\n
      if (o.level < LEVEL_OP) {\n
        return tests;\n
      } else {\n
        return this.wrapInBraces(tests);\n
      }\n
    };\n
\n
    In.prototype.compileLoopTest = function(o) {\n
      var fragments, ref, sub, _ref4;\n
      _ref4 = this.object.cache(o, LEVEL_LIST), sub = _ref4[0], ref = _ref4[1];\n
      fragments = [].concat(this.makeCode(utility(\'indexOf\') + ".call("), this.array.compileToFragments(o, LEVEL_LIST), this.makeCode(", "), ref, this.makeCode(") " + (this.negated ? \'< 0\' : \'>= 0\')));\n
      if (fragmentsToText(sub) === fragmentsToText(ref)) {\n
        return fragments;\n
      }\n
      fragments = sub.concat(this.makeCode(\', \'), fragments);\n
      if (o.level < LEVEL_LIST) {\n
        return fragments;\n
      } else {\n
        return this.wrapInBraces(fragments);\n
      }\n
    };\n
\n
    In.prototype.toString = function(idt) {\n
      return In.__super__.toString.call(this, idt, this.constructor.name + (this.negated ? \'!\' : \'\'));\n
    };\n
\n
    return In;\n
\n
  })(Base);\n
\n
  exports.Try = Try = (function(_super) {\n
    __extends(Try, _super);\n
\n
    function Try(attempt, errorVariable, recovery, ensure) {\n
      this.attempt = attempt;\n
      this.errorVariable = errorVariable;\n
      this.recovery = recovery;\n
      this.ensure = ensure;\n
    }\n
\n
    Try.prototype.children = [\'attempt\', \'recovery\', \'ensure\'];\n
\n
    Try.prototype.isStatement = YES;\n
\n
    Try.prototype.jumps = function(o) {\n
      var _ref4;\n
      return this.attempt.jumps(o) || ((_ref4 = this.recovery) != null ? _ref4.jumps(o) : void 0);\n
    };\n
\n
    Try.prototype.makeReturn = function(res) {\n
      if (this.attempt) {\n
        this.attempt = this.attempt.makeReturn(res);\n
      }\n
      if (this.recovery) {\n
        this.recovery = this.recovery.makeReturn(res);\n
      }\n
      return this;\n
    };\n
\n
    Try.prototype.compileNode = function(o) {\n
      var catchPart, ensurePart, placeholder, tryPart;\n
      o.indent += TAB;\n
      tryPart = this.attempt.compileToFragments(o, LEVEL_TOP);\n
      catchPart = this.recovery ? (placeholder = new Literal(\'_error\'), this.errorVariable ? this.recovery.unshift(new Assign(this.errorVariable, placeholder)) : void 0, [].concat(this.makeCode(" catch ("), placeholder.compileToFragments(o), this.makeCode(") {\\n"), this.recovery.compileToFragments(o, LEVEL_TOP), this.makeCode("\\n" + this.tab + "}"))) : !(this.ensure || this.recovery) ? [this.makeCode(\' catch (_error) {}\')] : [];\n
      ensurePart = this.ensure ? [].concat(this.makeCode(" finally {\\n"), this.ensure.compileToFragments(o, LEVEL_TOP), this.makeCode("\\n" + this.tab + "}")) : [];\n
      return [].concat(this.makeCode("" + this.tab + "try {\\n"), tryPart, this.makeCode("\\n" + this.tab + "}"), catchPart, ensurePart);\n
    };\n
\n
    return Try;\n
\n
  })(Base);\n
\n
  exports.Throw = Throw = (function(_super) {\n
    __extends(Throw, _super);\n
\n
    function Throw(expression) {\n
      this.expression = expression;\n
    }\n
\n
    Throw.prototype.children = [\'expression\'];\n
\n
    Throw.prototype.isStatement = YES;\n
\n
    Throw.prototype.jumps = NO;\n
\n
    Throw.prototype.makeReturn = THIS;\n
\n
    Throw.prototype.compileNode = function(o) {\n
      return [].concat(this.makeCode(this.tab + "throw "), this.expression.compileToFragments(o), this.makeCode(";"));\n
    };\n
\n
    return Throw;\n
\n
  })(Base);\n
\n
  exports.Existence = Existence = (function(_super) {\n
    __extends(Existence, _super);\n
\n
    function Existence(expression) {\n
      this.expression = expression;\n
    }\n
\n
    Existence.prototype.children = [\'expression\'];\n
\n
    Existence.prototype.invert = NEGATE;\n
\n
    Existence.prototype.compileNode = function(o) {\n
      var cmp, cnj, code, _ref4;\n
      this.expression.front = this.front;\n
      code = this.expression.compile(o, LEVEL_OP);\n
      if (IDENTIFIER.test(code) && !o.scope.check(code)) {\n
        _ref4 = this.negated ? [\'===\', \'||\'] : [\'!==\', \'&&\'], cmp = _ref4[0], cnj = _ref4[1];\n
        code = "typeof " + code + " " + cmp + " \\"undefined\\" " + cnj + " " + code + " " + cmp + " null";\n
      } else {\n
        code = "" + code + " " + (this.negated ? \'==\' : \'!=\') + " null";\n
      }\n
      return [this.makeCode(o.level <= LEVEL_COND ? code : "(" + code + ")")];\n
    };\n
\n
    return Existence;\n
\n
  })(Base);\n
\n
  exports.Parens = Parens = (function(_super) {\n
    __extends(Parens, _super);\n
\n
    function Parens(body) {\n
      this.body = body;\n
    }\n
\n
    Parens.prototype.children = [\'body\'];\n
\n
    Parens.prototype.unwrap = function() {\n
      return this.body;\n
    };\n
\n
    Parens.prototype.isComplex = function() {\n
      return this.body.isComplex();\n
    };\n
\n
    Parens.prototype.compileNode = function(o) {\n
      var bare, expr, fragments;\n
      expr = this.body.unwrap();\n
      if (expr instanceof Value && expr.isAtomic()) {\n
        expr.front = this.front;\n
        return expr.compileToFragments(o);\n
      }\n
      fragments = expr.compileToFragments(o, LEVEL_PAREN);\n
      bare = o.level < LEVEL_OP && (expr instanceof Op || expr instanceof Call || (expr instanceof For && expr.returns));\n
      if (bare) {\n
        return fragments;\n
      } else {\n
        return this.wrapInBraces(fragments);\n
      }\n
    };\n
\n
    return Parens;\n
\n
  })(Base);\n
\n
  exports.For = For = (function(_super) {\n
    __extends(For, _super);\n
\n
    function For(body, source) {\n
      var _ref4;\n
      this.source = source.source, this.guard = source.guard, this.step = source.step, this.name = source.name, this.index = source.index;\n
      this.body = Block.wrap([body]);\n
      this.own = !!source.own;\n
      this.object = !!source.object;\n
      if (this.object) {\n
        _ref4 = [this.index, this.name], this.name = _ref4[0], this.index = _ref4[1];\n
      }\n
      if (this.index instanceof Value) {\n
        this.index.error(\'index cannot be a pattern matching expression\');\n
      }\n
      this.range = this.source instanceof Value && this.source.base instanceof Range && !this.source.properties.length;\n
      this.pattern = this.name instanceof Value;\n
      if (this.range && this.index) {\n
        this.index.error(\'indexes do not apply to range loops\');\n
      }\n
      if (this.range && this.pattern) {\n
        this.name.error(\'cannot pattern match over range loops\');\n
      }\n
      if (this.own && !this.object) {\n
        this.index.error(\'cannot use own with for-in\');\n
      }\n
      this.returns = false;\n
    }\n
\n
    For.prototype.children = [\'body\', \'source\', \'guard\', \'step\'];\n
\n
    For.prototype.compileNode = function(o) {\n
      var body, bodyFragments, compare, compareDown, declare, declareDown, defPart, defPartFragments, down, forPartFragments, guardPart, idt1, increment, index, ivar, kvar, kvarAssign, lastJumps, lvar, name, namePart, ref, resultPart, returnResult, rvar, scope, source, step, stepNum, stepVar, svar, varPart, _ref4, _ref5;\n
      body = Block.wrap([this.body]);\n
      lastJumps = (_ref4 = last(body.expressions)) != null ? _ref4.jumps() : void 0;\n
      if (lastJumps && lastJumps instanceof Return) {\n
        this.returns = false;\n
      }\n
      source = this.range ? this.source.base : this.source;\n
      scope = o.scope;\n
      name = this.name && (this.name.compile(o, LEVEL_LIST));\n
      index = this.index && (this.index.compile(o, LEVEL_LIST));\n
      if (name && !this.pattern) {\n
        scope.find(name);\n
      }\n
      if (index) {\n
        scope.find(index);\n
      }\n
      if (this.returns) {\n
        rvar = scope.freeVariable(\'results\');\n
      }\n
      ivar = (this.object && index) || scope.freeVariable(\'i\');\n
      kvar = (this.range && name) || index || ivar;\n
      kvarAssign = kvar !== ivar ? "" + kvar + " = " : "";\n
      if (this.step && !this.range) {\n
        _ref5 = this.cacheToCodeFragments(this.step.cache(o, LEVEL_LIST)), step = _ref5[0], stepVar = _ref5[1];\n
        stepNum = stepVar.match(SIMPLENUM);\n
      }\n
      if (this.pattern) {\n
        name = ivar;\n
      }\n
      varPart = \'\';\n
      guardPart = \'\';\n
      defPart = \'\';\n
      idt1 = this.tab + TAB;\n
      if (this.range) {\n
        forPartFragments = source.compileToFragments(merge(o, {\n
          index: ivar,\n
          name: name,\n
          step: this.step\n
        }));\n
      } else {\n
        svar = this.source.compile(o, LEVEL_LIST);\n
        if ((name || this.own) && !IDENTIFIER.test(svar)) {\n
          defPart += "" + this.tab + (ref = scope.freeVariable(\'ref\')) + " = " + svar + ";\\n";\n
          svar = ref;\n
        }\n
        if (name && !this.pattern) {\n
          namePart = "" + name + " = " + svar + "[" + kvar + "]";\n
        }\n
        if (!this.object) {\n
          if (step !== stepVar) {\n
            defPart += "" + this.tab + step + ";\\n";\n
          }\n
          if (!(this.step && stepNum && (down = +stepNum < 0))) {\n
            lvar = scope.freeVariable(\'len\');\n
          }\n
          declare = "" + kvarAssign + ivar + " = 0, " + lvar + " = " + svar + ".length";\n
          declareDown = "" + kvarAssign + ivar + " = " + svar + ".length - 1";\n
          compare = "" + ivar + " < " + lvar;\n
          compareDown = "" + ivar + " >= 0";\n
          if (this.step) {\n
            if (stepNum) {\n
              if (down) {\n
                compare = compareDown;\n
                declare = declareDown;\n
              }\n
            } else {\n
              compare = "" + stepVar + " > 0 ? " + compare + " : " + compareDown;\n
              declare = "(" + stepVar + " > 0 ? (" + declare + ") : " + declareDown + ")";\n
            }\n
            increment = "" + ivar + " += " + stepVar;\n
          } else {\n
            increment = "" + (kvar !== ivar ? "++" + ivar : "" + ivar + "++");\n
          }\n
          forPartFragments = [this.makeCode("" + declare + "; " + compare + "; " + kvarAssign + increment)];\n
        }\n
      }\n
      if (this.returns) {\n
        resultPart = "" + this.tab + rvar + " = [];\\n";\n
        returnResult = "\\n" + this.tab + "return " + rvar + ";";\n
        body.makeReturn(rvar);\n
      }\n
      if (this.guard) {\n
        if (body.expressions.length > 1) {\n
          body.expressions.unshift(new If((new Parens(this.guard)).invert(), new Literal("continue")));\n
        } else {\n
          if (this.guard) {\n
            body = Block.wrap([new If(this.guard, body)]);\n
          }\n
        }\n
      }\n
      if (this.pattern) {\n
        body.expressions.unshift(new Assign(this.name, new Literal("" + svar + "[" + kvar + "]")));\n
      }\n
      defPartFragments = [].concat(this.makeCode(defPart), this.pluckDirectCall(o, body));\n
      if (namePart) {\n
        varPart = "\\n" + idt1 + namePart + ";";\n
      }\n
      if (this.object) {\n
        forPartFragments = [this.makeCode("" + kvar + " in " + svar)];\n
        if (this.own) {\n
          guardPart = "\\n" + idt1 + "if (!" + (utility(\'hasProp\')) + ".call(" + svar + ", " + kvar + ")) continue;";\n
        }\n
      }\n
      bodyFragments = body.compileToFragments(merge(o, {\n
        indent: idt1\n
      }), LEVEL_TOP);\n
      if (bodyFragments && (bodyFragments.length > 0)) {\n
        bodyFragments = [].concat(this.makeCode("\\n"), bodyFragments, this.makeCode("\\n"));\n
      }\n
      return [].concat(defPartFragments, this.makeCode("" + (resultPart || \'\') + this.tab + "for ("), forPartFragments, this.makeCode(") {" + guardPart + varPart), bodyFragments, this.makeCode("" + this.tab + "}" + (returnResult || \'\')));\n
    };\n
\n
    For.prototype.pluckDirectCall = function(o, body) {\n
      var base, defs, expr, fn, idx, ref, val, _i, _len, _ref4, _ref5, _ref6, _ref7, _ref8, _ref9;\n
      defs = [];\n
      _ref4 = body.expressions;\n
      for (idx = _i = 0, _len = _ref4.length; _i < _len; idx = ++_i) {\n
        expr = _ref4[idx];\n
        expr = expr.unwrapAll();\n
        if (!(expr instanceof Call)) {\n
          continue;\n
        }\n
        val = expr.variable.unwrapAll();\n
        if (!((val instanceof Code) || (val instanceof Value && ((_ref5 = val.base) != null ? _ref5.unwrapAll() : void 0) instanceof Code && val.properties.length === 1 && ((_ref6 = (_ref7 = val.properties[0].name) != null ? _ref7.value : void 0) === \'call\' || _ref6 === \'apply\')))) {\n
          continue;\n
        }\n
        fn = ((_ref8 = val.base) != null ? _ref8.unwrapAll() : void 0) || val;\n
        ref = new Literal(o.scope.freeVariable(\'fn\'));\n
        base = new Value(ref);\n
        if (val.base) {\n
          _ref9 = [base, val], val.base = _ref9[0], base = _ref9[1];\n
        }\n
        body.expressions[idx] = new Call(base, expr.args);\n
        defs = defs.concat(this.makeCode(this.tab), new Assign(ref, fn).compileToFragments(o, LEVEL_TOP), this.makeCode(\';\\n\'));\n
      }\n
      return defs;\n
    };\n
\n
    return For;\n
\n
  })(While);\n
\n
  exports.Switch = Switch = (function(_super) {\n
    __extends(Switch, _super);\n
\n
    function Switch(subject, cases, otherwise) {\n
      this.subject = subject;\n
      this.cases = cases;\n
      this.otherwise = otherwise;\n
    }\n
\n
    Switch.prototype.children = [\'subject\', \'cases\', \'otherwise\'];\n
\n
    Switch.prototype.isStatement = YES;\n
\n
    Switch.prototype.jumps = function(o) {\n
      var block, conds, _i, _len, _ref4, _ref5, _ref6;\n
      if (o == null) {\n
        o = {\n
          block: true\n
        };\n
      }\n
      _ref4 = this.cases;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        _ref5 = _ref4[_i], conds = _ref5[0], block = _ref5[1];\n
        if (block.jumps(o)) {\n
          return block;\n
        }\n
      }\n
      return (_ref6 = this.otherwise) != null ? _ref6.jumps(o) : void 0;\n
    };\n
\n
    Switch.prototype.makeReturn = function(res) {\n
      var pair, _i, _len, _ref4, _ref5;\n
      _ref4 = this.cases;\n
      for (_i = 0, _len = _ref4.length; _i < _len; _i++) {\n
        pair = _ref4[_i];\n
        pair[1].makeReturn(res);\n
      }\n
      if (res) {\n
        this.otherwise || (this.otherwise = new Block([new Literal(\'void 0\')]));\n
      }\n
      if ((_ref5 = this.otherwise) != null) {\n
        _ref5.makeReturn(res);\n
      }\n
      return this;\n
    };\n
\n
    Switch.prototype.compileNode = function(o) {\n
      var block, body, cond, conditions, expr, fragments, i, idt1, idt2, _i, _j, _len, _len1, _ref4, _ref5, _ref6;\n
      idt1 = o.indent + TAB;\n
      idt2 = o.indent = idt1 + TAB;\n
      fragments = [].concat(this.makeCode(this.tab + "switch ("), (this.subject ? this.subject.compileToFragments(o, LEVEL_PAREN) : this.makeCode("false")), this.makeCode(") {\\n"));\n
      _ref4 = this.cases;\n
      for (i = _i = 0, _len = _ref4.length; _i < _len; i = ++_i) {\n
        _ref5 = _ref4[i], conditions = _ref5[0], block = _ref5[1];\n
        _ref6 = flatten([conditions]);\n
        for (_j = 0, _len1 = _ref6.length; _j < _len1; _j++) {\n
          cond = _ref6[_j];\n
          if (!this.subject) {\n
            cond = cond.invert();\n
          }\n
          fragments = fragments.concat(this.makeCode(idt1 + "case "), cond.compileToFragments(o, LEVEL_PAREN), this.makeCode(":\\n"));\n
        }\n
        if ((body = block.compileToFragments(o, LEVEL_TOP)).length > 0) {\n
          fragments = fragments.concat(body, this.makeCode(\'\\n\'));\n
        }\n
        if (i === this.cases.length - 1 && !this.otherwise) {\n
          break;\n
        }\n
        expr = this.lastNonComment(block.expressions);\n
        if (expr instanceof Return || (expr instanceof Literal && expr.jumps() && expr.value !== \'debugger\')) {\n
          continue;\n
        }\n
        fragments.push(cond.makeCode(idt2 + \'break;\\n\'));\n
      }\n
      if (this.otherwise && this.otherwise.expressions.length) {\n
        fragments.push.apply(fragments, [this.makeCode(idt1 + "default:\\n")].concat(__slice.call(this.otherwise.compileToFragments(o, LEVEL_TOP)), [this.makeCode("\\n")]));\n
      }\n
      fragments.push(this.makeCode(this.tab + \'}\'));\n
      return fragments;\n
    };\n
\n
    return Switch;\n
\n
  })(Base);\n
\n
  exports.If = If = (function(_super) {\n
    __extends(If, _super);\n
\n
    function If(condition, body, options) {\n
      this.body = body;\n
      if (options == null) {\n
        options = {};\n
      }\n
      this.condition = options.type === \'unless\' ? condition.invert() : condition;\n
      this.elseBody = null;\n
      this.isChain = false;\n
      this.soak = options.soak;\n
    }\n
\n
    If.prototype.children = [\'condition\', \'body\', \'elseBody\'];\n
\n
    If.prototype.bodyNode = function() {\n
      var _ref4;\n
      return (_ref4 = this.body) != null ? _ref4.unwrap() : void 0;\n
    };\n
\n
    If.prototype.elseBodyNode = function() {\n
      var _ref4;\n
      return (_ref4 = this.elseBody) != null ? _ref4.unwrap() : void 0;\n
    };\n
\n
    If.prototype.addElse = function(elseBody) {\n
      if (this.isChain) {\n
        this.elseBodyNode().addElse(elseBody);\n
      } else {\n
        this.isChain = elseBody instanceof If;\n
        this.elseBody = this.ensureBlock(elseBody);\n
        this.elseBody.updateLocationDataIfMissing(elseBody.locationData);\n
      }\n
      return this;\n
    };\n
\n
    If.prototype.isStatement = function(o) {\n
      var _ref4;\n
      return (o != null ? o.level : void 0) === LEVEL_TOP || this.bodyNode().isStatement(o) || ((_ref4 = this.elseBodyNode()) != null ? _ref4.isStatement(o) : void 0);\n
    };\n
\n
    If.prototype.jumps = function(o) {\n
      var _ref4;\n
      return this.body.jumps(o) || ((_ref4 = this.elseBody) != null ? _ref4.jumps(o) : void 0);\n
    };\n
\n
    If.prototype.compileNode = function(o) {\n
      if (this.isStatement(o)) {\n
        return this.compileStatement(o);\n
      } else {\n
        return this.compileExpression(o);\n
      }\n
    };\n
\n
    If.prototype.makeReturn = function(res) {\n
      if (res) {\n
        this.elseBody || (this.elseBody = new Block([new Literal(\'void 0\')]));\n
      }\n
      this.body && (this.body = new Block([this.body.makeReturn(res)]));\n
      this.elseBody && (this.elseBody = new Block([this.elseBody.makeReturn(res)]));\n
      return this;\n
    };\n
\n
    If.prototype.ensureBlock = function(node) {\n
      if (node instanceof Block) {\n
        return node;\n
      } else {\n
        return new Block([node]);\n
      }\n
    };\n
\n
    If.prototype.compileStatement = function(o) {\n
      var answer, body, child, cond, exeq, ifPart, indent;\n
      child = del(o, \'chainChild\');\n
      exeq = del(o, \'isExistentialEquals\');\n
      if (exeq) {\n
        return new If(this.condition.invert(), this.elseBodyNode(), {\n
          type: \'if\'\n
        }).compileToFragments(o);\n
      }\n
      indent = o.indent + TAB;\n
      cond = this.condition.compileToFragments(o, LEVEL_PAREN);\n
      body = this.ensureBlock(this.body).compileToFragments(merge(o, {\n
        indent: indent\n
      }));\n
      ifPart = [].concat(this.makeCode("if ("), cond, this.makeCode(") {\\n"), body, this.makeCode("\\n" + this.tab + "}"));\n
      if (!child) {\n
        ifPart.unshift(this.makeCode(this.tab));\n
      }\n
      if (!this.elseBody) {\n
        return ifPart;\n
      }\n
      answer = ifPart.concat(this.makeCode(\' else \'));\n
      if (this.isChain) {\n
        o.chainChild = true;\n
        answer = answer.concat(this.elseBody.unwrap().compileToFragments(o, LEVEL_TOP));\n
      } else {\n
        answer = answer.concat(this.makeCode("{\\n"), this.elseBody.compileToFragments(merge(o, {\n
          indent: indent\n
        }), LEVEL_TOP), this.makeCode("\\n" + this.tab + "}"));\n
      }\n
      return answer;\n
    };\n
\n
    If.prototype.compileExpression = function(o) {\n
      var alt, body, cond, fragments;\n
      cond = this.condition.compileToFragments(o, LEVEL_COND);\n
      body = this.bodyNode().compileToFragments(o, LEVEL_LIST);\n
      alt = this.elseBodyNode() ? this.elseBodyNode().compileToFragments(o, LEVEL_LIST) : [this.makeCode(\'void 0\')];\n
      fragments = cond.concat(this.makeCode(" ? "), body, this.makeCode(" : "), alt);\n
      if (o.level >= LEVEL_COND) {\n
        return this.wrapInBraces(fragments);\n
      } else {\n
        return fragments;\n
      }\n
    };\n
\n
    If.prototype.unfoldSoak = function() {\n
      return this.soak && this;\n
    };\n
\n
    return If;\n
\n
  })(Base);\n
\n
  Closure = {\n
    wrap: function(expressions, statement, noReturn) {\n
      var args, argumentsNode, call, func, meth;\n
      if (expressions.jumps()) {\n
        return expressions;\n
      }\n
      func = new Code([], Block.wrap([expressions]));\n
      args = [];\n
      argumentsNode = expressions.contains(this.isLiteralArguments);\n
      if (argumentsNode && expressions.classBody) {\n
        argumentsNode.error("Class bodies shouldn\'t reference arguments");\n
      }\n
      if (argumentsNode || expressions.contains(this.isLiteralThis)) {\n
        meth = new Literal(argumentsNode ? \'apply\' : \'call\');\n
        args = [new Literal(\'this\')];\n
        if (argumentsNode) {\n
          args.push(new Literal(\'arguments\'));\n
        }\n
        func = new Value(func, [new Access(meth)]);\n
      }\n
      func.noReturn = noReturn;\n
      call = new Call(func, args);\n
      if (statement) {\n
        return Block.wrap([call]);\n
      } else {\n
        return call;\n
      }\n
    },\n
    isLiteralArguments: function(node) {\n
      return node instanceof Literal && node.value === \'arguments\' && !node.asKey;\n
    },\n
    isLiteralThis: function(node) {\n
      return (node instanceof Literal && node.value === \'this\' && !node.asKey) || (node instanceof Code && node.bound) || (node instanceof Call && node.isSuper);\n
    }\n
  };\n
\n
  unfoldSoak = function(o, parent, name) {\n
    var ifn;\n
    if (!(ifn = parent[name].unfoldSoak(o))) {\n
      return;\n
    }\n
    parent[name] = ifn.body;\n
    ifn.body = new Value(parent);\n
    return ifn;\n
  };\n
\n
  UTILITIES = {\n
    "extends": function() {\n
      return "function(child, parent) { for (var key in parent) { if (" + (utility(\'hasProp\')) + ".call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; }";\n
    },\n
    bind: function() {\n
      return \'function(fn, me){ return function(){ return fn.apply(me, arguments); }; }\';\n
    },\n
    indexOf: function() {\n
      return "[].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; }";\n
    },\n
    hasProp: function() {\n
      return \'{}.hasOwnProperty\';\n
    },\n
    slice: function() {\n
      return \'[].slice\';\n
    }\n
  };\n
\n
  LEVEL_TOP = 1;\n
\n
  LEVEL_PAREN = 2;\n
\n
  LEVEL_LIST = 3;\n
\n
  LEVEL_COND = 4;\n
\n
  LEVEL_OP = 5;\n
\n
  LEVEL_ACCESS = 6;\n
\n
  TAB = \'  \';\n
\n
  IDENTIFIER_STR = "[$A-Za-z_\\\\x7f-\\\\uffff][$\\\\w\\\\x7f-\\\\uffff]*";\n
\n
  IDENTIFIER = RegExp("^" + IDENTIFIER_STR + "$");\n
\n
  SIMPLENUM = /^[+-]?\\d+$/;\n
\n
  METHOD_DEF = RegExp("^(?:(" + IDENTIFIER_STR + ")\\\\.prototype(?:\\\\.(" + IDENTIFIER_STR + ")|\\\\[(\\"(?:[^\\\\\\\\\\"\\\\r\\\\n]|\\\\\\\\.)*\\"|\'(?:[^\\\\\\\\\'\\\\r\\\\n]|\\\\\\\\.)*\')\\\\]|\\\\[(0x[\\\\da-fA-F]+|\\\\d*\\\\.?\\\\d+(?:[eE][+-]?\\\\d+)?)\\\\]))|(" + IDENTIFIER_STR + ")$");\n
\n
  IS_STRING = /^[\'"]/;\n
\n
  utility = function(name) {\n
    var ref;\n
    ref = "__" + name;\n
    Scope.root.assign(ref, UTILITIES[name]());\n
    return ref;\n
  };\n
\n
  multident = function(code, tab) {\n
    code = code.replace(/\\n/g, \'$&\' + tab);\n
    return code.replace(/\\s+$/, \'\');\n
  };\n
\n
\n
});\n
\n
define(\'ace/mode/coffee/scope\', [\'require\', \'exports\', \'module\' , \'ace/mode/coffee/helpers\'], function(require, exports, module) {\n
\n
  var Scope, extend, last, _ref;\n
\n
  _ref = require(\'./helpers\'), extend = _ref.extend, last = _ref.last;\n
\n
  exports.Scope = Scope = (function() {\n
    Scope.root = null;\n
\n
    function Scope(parent, expressions, method) {\n
      this.parent = parent;\n
      this.expressions = expressions;\n
      this.method = method;\n
      this.variables = [\n
        {\n
          name: \'arguments\',\n
          type: \'arguments\'\n
        }\n
      ];\n
      this.positions = {};\n
      if (!this.parent) {\n
        Scope.root = this;\n
      }\n
    }\n
\n
    Scope.prototype.add = function(name, type, immediate) {\n
      if (this.shared && !immediate) {\n
        return this.parent.add(name, type, immediate);\n
      }\n
      if (Object.prototype.hasOwnProperty.call(this.positions, name)) {\n
        return this.variables[this.positions[name]].type = type;\n
      } else {\n
        return this.positions[name] = this.variables.push({\n
          name: name,\n
          type: type\n
        }) - 1;\n
      }\n
    };\n
\n
    Scope.prototype.namedMethod = function() {\n
      var _ref1;\n
      if (((_ref1 = this.method) != null ? _ref1.name : void 0) || !this.parent) {\n
        return this.method;\n
      }\n
      return this.parent.namedMethod();\n
    };\n
\n
    Scope.prototype.find = function(name) {\n
      if (this.check(name)) {\n
        return true;\n
      }\n
      this.add(name, \'var\');\n
      return false;\n
    };\n
\n
    Scope.prototype.parameter = function(name) {\n
      if (this.shared && this.parent.check(name, true)) {\n
        return;\n
      }\n
      return this.add(name, \'param\');\n
    };\n
\n
    Scope.prototype.check = function(name) {\n
      var _ref1;\n
      return !!(this.type(name) || ((_ref1 = this.parent) != null ? _ref1.check(name) : void 0));\n
    };\n
\n
    Scope.prototype.temporary = function(name, index) {\n
      if (name.length > 1) {\n
        return \'_\' + name + (index > 1 ? index - 1 : \'\');\n
      } else {\n
        return \'_\' + (index + parseInt(name, 36)).toString(36).replace(/\\d/g, \'a\');\n
      }\n
    };\n
\n
    Scope.prototype.type = function(name) {\n
      var v, _i, _len, _ref1;\n
      _ref1 = this.variables;\n
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {\n
        v = _ref1[_i];\n
        if (v.name === name) {\n
          return v.type;\n
        }\n
      }\n
      return null;\n
    };\n
\n
    Scope.prototype.freeVariable = function(name, reserve) {\n
      var index, temp;\n
      if (reserve == null) {\n
        reserve = true;\n
      }\n
      index = 0;\n
      while (this.check((temp = this.temporary(name, index)))) {\n
        index++;\n
      }\n
      if (reserve) {\n
        this.add(temp, \'var\', true);\n
      }\n
      return temp;\n
    };\n
\n
    Scope.prototype.assign = function(name, value) {\n
      this.add(name, {\n
        value: value,\n
        assigned: true\n
      }, true);\n
      return this.hasAssignments = true;\n
    };\n
\n
    Scope.prototype.hasDeclarations = function() {\n
      return !!this.declaredVariables().length;\n
    };\n
\n
    Scope.prototype.declaredVariables = function() {\n
      var realVars, tempVars, v, _i, _len, _ref1;\n
      realVars = [];\n
      tempVars = [];\n
      _ref1 = this.variables;\n
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {\n
        v = _ref1[_i];\n
        if (v.type === \'var\') {\n
          (v.name.charAt(0) === \'_\' ? tempVars : realVars).push(v.name);\n
        }\n
      }\n
      return realVars.sort().concat(tempVars.sort());\n
    };\n
\n
    Scope.prototype.assignedVariables = function() {\n
      var v, _i, _len, _ref1, _results;\n
      _ref1 = this.variables;\n
      _results = [];\n
      for (_i = 0, _len = _ref1.length; _i < _len; _i++) {\n
        v = _ref1[_i];\n
        if (v.type.assigned) {\n
          _results.push("" + v.name + " = " + v.type.value);\n
        }\n
      }\n
      return _results;\n
    };\n
\n
    return Scope;\n
\n
  })();\n
\n
\n
});

]]></string> </value>
        </item>
        <item>
            <key> <string>next</string> </key>
            <value>
              <none/>
            </value>
        </item>
      </dictionary>
    </pickle>
  </record>
</ZopeData>
