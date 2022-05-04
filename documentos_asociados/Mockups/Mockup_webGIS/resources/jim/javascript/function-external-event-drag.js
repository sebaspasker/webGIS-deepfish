/*!
 * Multi-Touch enabled jQuery.event.drag
 * http://addictivity.de/jquery-drag-event-plugin-multi-touch/
 * @license Open Source MIT
 * @author Fabian Arnold <http://addictivity.de/>
 * @release 0.1
 *
 * @original-license
 * http://www.shamasis.net/projects/jquery-drag-touch/
 * @license Open Source MIT
 * @author Shamasis Bhattacharya <http://www.shamasis.net/>
 * @release 2.0.1
 *
 * @original-license
 * jquery.event.drag - v 2.0.0
 * Copyright (c) 2010 Three Dub Media - http://threedubmedia.com
 * Open Source MIT License - http://threedubmedia.com/code/license
 */
(function( $ ){

    // add the jquery instance method
    $.fn.drag = function( str, arg, opts ){
        // figure out the event type
        var type = typeof str == "string" ? str : "",
        // figure out the event handler...
        fn = $.isFunction( str ) ? str : $.isFunction( arg ) ? arg : null;
        // fix the event type
        if ( type.indexOf("drag") !== 0 )
            type = "drag"+ type;
        // were options passed
        opts = ( str == fn ? arg : opts ) || {};
        // trigger or bind event handler
        return fn ? this.bind( type, opts, fn ) : this.trigger( type );
    };

    // local refs (increase compression)
    var $event = $.event,
    hasTouch = 'ontouchstart' in document.documentElement,
    initBindings = hasTouch ? 'touchstart' : 'mousedown',
    dragBindings = hasTouch ? 'touchmove touchend' : 'mousemove mouseup',
    touchEventXY = function (event, dd) {
        if (!dd.touchXY || !event.originalEvent) {
            return event;
        }

        // check whether mouse click or screentap
        var touches = event.originalEvent.changedTouches ||
        event.originalEvent.touches;
        if (touches && touches.length) {
            $.extend(event, touches[0]);
        }
        return event;
    },

    $special = $event.special,
    // configure the drag special event
    drag = $special.drag = {

        // these are the default settings
        defaults: {
            which: 1, // mouse button pressed to start drag sequence
            distance: 0.001, // distance dragged before dragstart
            // JIM MODIFICATION 
            //not: ':input', // selector to suppress dragging on target elements
            //not: "[type='button'],[type='checkbox'],[type='file'],[type='hidden'],[type='image'],[type='password'],[type='radio'],[type='reset'],[type='submit'],[type='text'],select,textarea,button", // selector to suppress dragging on target elements adapted to deprecated :input selector
            not: "", // selector to suppress dragging on target elements
            handle: null, // selector to match handle target elements
            relative: false, // true to use "position", false to use "offset"
            drop: false, // false to suppress drop events, true or selector to allow
            click: false, // false to suppress click events after dragend (no proxy)
            touchXY: true // Make touch XY match event XY
        },

        // the key name for stored drag data
        datakey: "dragdata",

        // the namespace for internal live events
        livekey: "livedrag",

        // count bound related events
        add: function( obj ){
            // read the interaction data
            var data = $.data( this, drag.datakey ),
            // read any passed options
            opts = obj.data || {};
            // count another realted event
            data.related += 1;
            // bind the live "draginit" delegator
            if ( !data.live && obj.selector ){
                data.live = true;
                $event.add( this, "draginit."+ drag.livekey, drag.delegate );
            }
            // extend data options bound with this event
            // don't iterate "opts" in case it is a node
            $.each( drag.defaults, function( key, def ){
                if ( opts[ key ] !== undefined )
                    data[ key ] = opts[ key ];
            });
        },

        // forget unbound related events
        remove: function(){
            $.data( this, drag.datakey ).related -= 1;
        },

        // configure interaction, capture settings
        setup: function(){
            // check for related events
            if ( $.data( this, drag.datakey ) )
                return;
            // initialize the drag data with copied defaults
            var data = $.extend({
                related:0
            }, drag.defaults );
            // store the interaction data
            $.data( this, drag.datakey, data );
            // bind the mousedown event, which starts drag interactions
            $event.add( this, initBindings, drag.init, data );
            // prevent image dragging in IE...
            if ( this.attachEvent )
                this.attachEvent("ondragstart", drag.dontstart );
        },

        // destroy configured interaction
        teardown: function(){
            // check for related events
            if ( $.data( this, drag.datakey ).related )
                return;
            // remove the stored data
            $.removeData( this, drag.datakey );
            // remove the mousedown event
            $event.remove( this, initBindings, drag.init );
            // remove the "live" delegation
            $event.remove( this, "draginit", drag.delegate );
            // enable text selection
            drag.textselect( true );
            // un-prevent image dragging in IE...
            if ( this.detachEvent )
                this.detachEvent("ondragstart", drag.dontstart );
        },

        // initialize the interaction
        init: function( event ){
            // the drag/drop interaction data
            var dd = event.data, results,
            touches = event.originalEvent ? event.originalEvent.changedTouches ||
            event.originalEvent.touches : [];

            // check whether mouse click or screentap
            if (touches && touches.length) {
                // let the system handle multitouch operations like two finger scroll
                // and pinching
                if (touches.length > 1) {
                    return;
                }
                var pos_x = event.originalEvent.touches[0].pageX; // JIM MODIFICATION
                var pos_y = event.originalEvent.touches[0].pageY; // JIM MODIFICATION
            }
            else {
                // check the which directive
                if ( dd.which > 0 && event.which != dd.which ) {
                    return;
                }
                var pos_x = event.pageX; // JIM MODIFICATION
                var pos_y = event.pageY; // JIM MODIFICATION
            }

            // check for suppressed selector
            if ( $( event.target ).is( dd.not ) )
                return;
            // check for handle selector
            if ( dd.handle && !$( event.target ).closest( dd.handle, event.currentTarget ).length )
                return;
            // store/reset some initial attributes
            dd.propagates = 1;
            dd.interactions = [ drag.interaction( this, dd ) ];
            dd.target = event.target;
            dd.pageX = pos_x; // event.pageX JIM MODIFICATION
            dd.pageY = pos_y; // event.pageY JIM MODIFICATION
            dd.dragging = null;
            // handle draginit event...
            results = drag.hijack( event, "draginit", dd );
            //if ()
            // early cancel
            if ( !dd.propagates )
                return;
            // flatten the result set
            results = drag.flatten( results );
            // insert new interaction elements
            if ( results && results.length ){
                dd.interactions = [];
                $.each( results, function(){
                    dd.interactions.push( drag.interaction( this, dd ) );
                });
            }
            // remember how many interactions are propagating
            dd.propagates = dd.interactions.length;
            // locate and init the drop targets
            if ( dd.drop !== false && $special.drop )
                $special.drop.handler( event, dd );
            // disable text selection
            drag.textselect( false );
            // bind additional events...
            $event.add( document, dragBindings, drag.handler, dd );
            
            /* START JIM MODIFICATION: do not return false in order to propagate the event. 
             //Fix problems expanding dropdowns inside a container with a drag event defined.*/
              
            if(jQuery(event.target).is("select") || jQuery(event.target).is("input") || jQuery(event.target).is("textarea"))
			  return;
				
            // helps prevent text selection
             if (!hasTouch ) {
               return false;
             }
            /*END JIM MODIFICATION*/
        },
        // returns an interaction object
        interaction: function( elem, dd ){
            return {
                drag: elem,
                callback: new drag.callback(),
                droppable: [],
                offset: $( elem )[ dd.relative ? "position" : "offset" ]() || {
                    top:0,
                    left:0
                }
            };
        },
        // handle drag-releatd DOM events
        handler: function( event ){
            // read the data before hijacking anything
            var dd = event.data;
            // mousemove, check distance, start dragging
            if (!dd.dragging && (event.type === 'mousemove' || event.type === 'touchmove')) {
                //  drag tolerance, x² + y² = distance²
                if ( Math.pow(  event.pageX-dd.pageX, 2 ) + Math.pow(  event.pageY-dd.pageY, 2 ) < Math.pow( dd.distance, 2 ) )
                    return; // distance tolerance not reached
                event.target = dd.target; // force target from "mousedown" event (fix distance issue)
                drag.hijack( event, "dragstart", dd ); // trigger "dragstart"
                if ( dd.propagates ) // "dragstart" not rejected
                    dd.dragging = true; // activate interaction
            }
            // handle various events
            switch ( event.type ){
                // mousemove, dragging
                case 'touchmove':
                    // prevent touch device screen scrolling.
                    if (dd.dragging) {
                        event.preventDefault();
                        touchEventXY(event, dd);
                    }

                case 'mousemove':
                    if ( dd.dragging ){
                        // trigger "drag"
                        drag.hijack( event, "drag", dd );
                        if ( dd.propagates ){
                            // manage drop events
                            if ( dd.drop !== false && $special.drop )
                                $special.drop.handler( event, dd ); // "dropstart", "dropend"
                            break; // "drag" not rejected, stop
                        }
                        event.type = "mouseup"; // helps "drop" handler behave
                    }
                // mouseup, stop dragging
                case 'mouseup':
                case 'touchend':
                    $event.remove( document, dragBindings, drag.handler ); // remove page events
                    if ( dd.dragging ){
                        if ( dd.drop !== false && $special.drop )
                            $special.drop.handler( event, dd ); // "drop"
                        drag.hijack( event, "dragend", dd ); // trigger "dragend"
                    }
                    drag.textselect( true ); // enable text selection

                    // if suppressing click events...
                    if ( dd.click === false && dd.dragging ){
                        jQuery.event.triggered = "click"; // true JIM MODIFICATION
                        setTimeout(function(){
                            jQuery.event.triggered = undefined; // false JIM MODIFICATION
                        }, 20 );
                        dd.dragging = false; // deactivate element
                    }
                    break;
            }
        },

        /* START JIM MODIFICATION
           BASED ON http://groups.google.com/group/threedubmedia/browse_thread/thread/732d9537a0b33843/7cd4860bf943dee0?lnk=gst&q=1.7#7cd4860bf943dee0
        // identify potential delegate elements
        delegate: function( event ){
            // local refs
            var elems = [], target,
            // element event structure
            events = $.data( this, "events" ) || {};
            // query live events
            $.each( events.live || [], function( i, obj ){
                // no event type matches
                if ( obj.preType.indexOf("drag") !== 0 )
                    return;
                // locate the element to delegate
                target = $( event.target ).closest( obj.selector, event.currentTarget )[0];
                // no element found
                if ( !target )
                    return;
                // add an event handler
                $event.add( target, obj.origType+'.'+drag.livekey, obj.origHandler, obj.data );
                // remember new elements
                if ( $.inArray( target, elems ) < 0 )
                    elems.push( target );
            });
            // if there are no elements, break
            if ( !elems.length )
                return false;
            // return the matched results, and clenup when complete
            return $( elems ).bind("dragend."+ drag.livekey, function(){
                $event.remove( this, "."+ drag.livekey ); // cleanup delegation
            });
        },*/
        
        // identify potential delegate elements
        delegate: function( event ){
          // local refs
          var elems = [], target,
          // element event structure
          events = $._data( this, "events" ) || {}, key, i, liver; // JIM MODIFICATION: jQuery 1.8 deprecated jQuery.data("events") -> jQuery._data("events")
          // query live events
          for (key in events) {
            if (key.indexOf("drag") !== 0)
              continue;
            liver = events[key];
            for (i=0; i<liver.length; i++) {
              target = $( event.target ).closest( liver[i].selector, event.currentTarget )[0];
              if ( !target )
                continue;
              $event.add( target, liver[i].origType+'.'+drag.livekey, liver[i].origHandler || liver[i].handler, liver[i].data );
              // remember new elements
              if ( $.inArray( target, elems ) < 0 )
                elems.push( target );
            }
          }
          // if there are no elements, break
          if ( !elems.length )
            return false;
          // return the matched results, and clenup when complete
          return $( elems ).bind("dragend."+ drag.livekey, function(){
            $event.remove( this, "."+ drag.livekey ); // cleanup delegation
          });
        }, /* END JIM MODIFICATION */

        // re-use event object for custom events
        hijack: function( event, type, dd, x, elem ){
            // not configured
            if ( !dd )
                return;
            // remember the original event and type
            var orig = {
                event:event.originalEvent,
                type: event.type
            },
            // is the event drag related or drog related?
            mode = type.indexOf("drop") ? "drag" : "drop",
            // iteration vars
            result, i = x || 0, ia, $elems, callback,
            len = !isNaN( x ) ? x : dd.interactions.length;
            // modify the event type
            event.type = type;
            // copy the originalEvent as 'source event'
            event.sourceEvent = orig.event;
            // remove the original event
            event.originalEvent = null;
            // initialize the results
            dd.results = [];
            // handle each interacted element
            do if ( ia = dd.interactions[ i ] ){
                // validate the interaction
                if ( type !== "dragend" && ia.cancelled )
                    continue;
                // set the dragdrop properties on the event object
                callback = drag.properties( event, dd, ia );
                // prepare for more results
                ia.results = [];
                // handle each element
                $( elem || ia[ mode ] || dd.droppable ).each(function( p, subject ){
                    // identify drag or drop targets individually
                    callback.target = subject;
                    // handle the event
                    result = subject ? $event.handle.call( subject, event, callback ) : null;
                    // stop the drag interaction for this element
                    if ( result === false ){
                        if ( mode == "drag" ){
                            ia.cancelled = true;
                            dd.propagates -= 1;
                        }
                        if ( type == "drop" ){
                            ia[ mode ][p] = null;
                        }
                    }
                    // assign any dropinit elements
                    else if ( type == "dropinit" )
                        ia.droppable.push( drag.element( result ) || subject );
                    // accept a returned proxy element
                    if ( type == "dragstart" )
                        ia.proxy = $( drag.element( result ) || ia.drag )[0];
                    // remember this result
                    ia.results.push( result );
                    // forget the event result, for recycling
                    delete event.result;
                    // break on cancelled handler
                    if ( type !== "dropinit" )
                        return result;
                });
                // flatten the results
                dd.results[ i ] = drag.flatten( ia.results );
                // accept a set of valid drop targets
                if ( type == "dropinit" )
                    ia.droppable = drag.flatten( ia.droppable );
                // locate drop targets
                if ( type == "dragstart" && !ia.cancelled )
                    callback.update();
            }
            while ( ++i < len )
            // restore the original event & type
            event.type = orig.type;
            event.originalEvent = orig.event;
            // return all handler results
            return drag.flatten( dd.results );
        },

        // extend the callback object with drag/drop properties...
        properties: function( event, dd, ia ){
            var obj = ia.callback;
            // elements
            obj.drag = ia.drag;
            obj.proxy = ia.proxy || ia.drag;
            // starting mouse position
            obj.startX = dd.pageX;
            obj.startY = dd.pageY;
            // current distance dragged
            obj.deltaX = event.pageX - dd.pageX;
            obj.deltaY = event.pageY - dd.pageY;
            // original element position
            obj.originalX = ia.offset.left;
            obj.originalY = ia.offset.top;
            // adjusted element position
            obj.offsetX = event.pageX - ( dd.pageX - obj.originalX );
            obj.offsetY = event.pageY - ( dd.pageY - obj.originalY );
            // assign the drop targets information
            obj.drop = drag.flatten( ( ia.drop || [] ).slice() );
            obj.available = drag.flatten( ( ia.droppable || [] ).slice() );
            return obj;
        },

        // determine is the argument is an element or jquery instance
        element: function( arg ){
            if ( arg && ( arg.jquery || arg.nodeType == 1 ) )
                return arg;
        },

        // flatten nested jquery objects and arrays into a single dimension array
        flatten: function( arr ){
            return $.map( arr, function( member ){
                return member && member.jquery ? $.makeArray( member ) :
                member && member.length ? drag.flatten( member ) : member;
            });
        },

        // toggles text selection attributes ON (true) or OFF (false)
        textselect: function( bool ){
            $( document )[ bool ? "unbind" : "bind" ]("selectstart", drag.dontstart )
            .attr("unselectable", bool ? "off" : "on" )
            .css("MozUserSelect", bool ? "" : "none" );
        },

        // suppress "selectstart" and "ondragstart" events
        dontstart: function(){
            return false;
        },

        // a callback instance contructor
        callback: function(){}

    };

    // callback methods
    drag.callback.prototype = {
        update: function(){
            if ( $special.drop && this.available.length )
                $.each( this.available, function( i ){
                    $special.drop.locate( this, i );
                });
        }
    };

    // share the same special event configuration with related events...
    $special.draginit = $special.dragstart = $special.dragend = drag;
})( jQuery );