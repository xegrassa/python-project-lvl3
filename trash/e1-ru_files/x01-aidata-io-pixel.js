
	;(function(window, document) {
		var onDomReady = function (callback) {
				readyBound = false;
				onDomReady.isReady = false;
				if (typeof callback == 'function') {
					DOMReadyCallback = callback;
				}
				bindReady();
			},
			readyBound = false,
			DOMReadyCallback = function () {},
			DOMContentLoaded;
		onDomReady.isReady = false;
		var DOMReady = function () {
			if (!onDomReady.isReady) {
				if (!document.body) {
					setTimeout(DOMReady, 13);
					return;
				}
				onDomReady.isReady = true;
				DOMReadyCallback();
			}
		};
		var bindReady = function () {
			if (readyBound) {
				return;
			}
			readyBound = true;
			if (document.readyState === "complete") {
				DOMReady();
			}
			if (document.addEventListener) {
				document.addEventListener("DOMContentLoaded", DOMContentLoaded, false);
				window.addEventListener("load", DOMContentLoaded, false);
			} else if (document.attachEvent) {
				document.attachEvent("onreadystatechange", DOMContentLoaded);
				window.attachEvent("onload", DOMContentLoaded);
				var toplevel = false;
				try {
					toplevel = window.frameElement == null;
				} catch (e) {}
				if (document.documentElement.doScroll && toplevel) {
					doScrollCheck();
				}
			}
		};
		var doScrollCheck = function () {
			if (onDomReady.isReady) {
				return;
			}
			try {
				document.documentElement.doScroll("left");
			} catch (error) {
				setTimeout(doScrollCheck, 1);
				return;
			}
			DOMReady();
		};
		if (document.addEventListener) {
			DOMContentLoaded = function () {
				document.removeEventListener("DOMContentLoaded", DOMContentLoaded, false);
				DOMReady();
			};
		} else if (document.attachEvent) {
			DOMContentLoaded = function () {
				if (document.readyState === "complete") {
					document.detachEvent("onreadystatechange", DOMContentLoaded);
					DOMReady();
				}
			};
		}

		window.aidataSendEvent = function(value, type) {
			if(!type || !(/^[\x00-\x7F]*$/.test(type))) {
				console.error('The type parameter is required and must contain ASCII characters only.');
				return;
			}
			if(typeof value !== 'string' && typeof value !== 'number') {
				console.error('The value must be a string or a number.');
				return;
			}
			sendMessage({
				'event': 'custom',
				'type': type,
				'data': {
					'value': value
				}
			});
		}

		var jsCookie = getCookie('__upin') || 'N5CjIENBI+8RxjyDwrwFKQ';

		document.cookie = '__upin' + '=' + jsCookie + ";path=/;expires="+new Date(new Date().setFullYear(new Date().getFullYear()+2)).toUTCString()+((document.domain&&document.domain.match(/[^\.]*\.[^.]*$/))?";domain="+(document.domain.match(/[^\.]*\.[^.]*$/)[0]):"");

		function getCookie(name) {
			var matches = document.cookie.match(new RegExp(
				"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
			));
			return matches ? decodeURIComponent(matches[1]) : '';
		}

		var iframe = document.createElement('iframe');
		var src = 'http://x01.aidata.io/stats?pixel=7921581&v=1586516444329&pid=7921581&js=1&id=&bounce=1&pid=7921581&js=1&id=&sid=7ea84debd349438eb2f21a38c5cc827a&__upin=' + jsCookie + '&payload=';
		iframe.width = '0';
		iframe.height = '0';
		iframe.frameBorder = '0';
		iframe.style.position = 'absolute';
		iframe.style.left = '-9999px';
		function sendMessage(data) {
			var img = document.createElement('img');
			img.src = src + escape(JSON.stringify(data));
			iframe.contentDocument.body.appendChild(img);
		}
		var startVisitTime = Date.now();
		var heartBeatTimeout = 1000 * 10;
		function heartBeat() {
			sendMessage({
				'event': 'time_spent',
				'type': 'total',
				'data': {
					'value': Date.now() - startVisitTime
				}
			});
		}
		var links = ["http://cm.g.doubleclick.net/pixel?google_nid=aidata_ddp&back=1STPARTY&google_cm", "http://sync.1dmp.io/pixel.gif?cid=f3c5784e-9a1e-4a1c-887d-dfe2e0b8668b&pid=fe3f3a81-853f-42c7-992a-63a613fc388f&uid=N5CjIENBI%2B8RxjyDwrwFKQ&ru=http%3A//x01.aidata.io/0.gif%3Fpid%3D1STPARTY", "http://px.adhigh.net/p/cm/aidata?u=N5CjIENBI%2B8RxjyDwrwFKQ&back=1STPARTY", "http://counter.yadro.ru/id-redir/aidata.gif", "http://sync.crwdcntrl.net/map/c=7645/tp=AIDA/?http://x01.aidata.io/0.gif?pid=LOTAME&id=N5CjIENBI%2B8RxjyDwrwFKQ&back=1STPARTY", "http://sync.upravel.com/aidata/sync?back=1STPARTY", "http://aidata-sync.rutarget.ru/sync?back=1STPARTY", "http://cm.p.altergeo.ru/aidata?aid=N5CjIENBI%2B8RxjyDwrwFKQ&nc=6168&url=http%3A//x01.aidata.io/0.gif%3Fpid%3DALTERGEO%26id%3D%24%7BUSER_ID%7D%26rnd%3D%24%7BRANDOM%7D%26back%3D1STPARTY", "http://an.yandex.ru/mapuid/dmpaidatame/N5CjIENBI%2B8RxjyDwrwFKQ?sign=4184115494&location=http%3A//x01.aidata.io/0.gif%3Fpid%3D1STPARTY", "http://ad.mail.ru/cm.gif?p=18&id=N5CjIENBI%2B8RxjyDwrwFKQ", "http://ps.eyeota.net/pixel?pid=1mp75m0&t=gif&uid=N5CjIENBI%2B8RxjyDwrwFKQ"];
		var clicks_selectors = [];
		var views_selectors = [];
		var tmp_pid_id = '7921581';

		iframe.onload = function() {
			var w = window,
				d = document,
				e = d.documentElement,
				b = d.getElementsByTagName('body')[0];
			var windowY = w.innerHeight || e.clientHeight || b.clientHeight;
			var windowX = w.innerWidth || e.clientWidth || b.clientWidth;
			// Utils
			function escapeRegExp(string) {
				return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
			}

			function checkUrlPattern(url_pattern) {
				try {
					if(!url_pattern) {
						return true;
					}
					if(url_pattern[0] === '~') {
						var pattern = url_pattern.substr(1);
						var reg = new RegExp(pattern.split('*').map(escapeRegExp).join('.*'));
						var matchResult = window.location.href.match(reg);
						return matchResult && matchResult[0] === window.location.href;
					} else {
						return url_pattern === window.location.href
					}
				} catch(e) {
					sendMessage({
						'event': 'error',
						'type': 'click',
						'data': {
							'message': 'bad url_pattern selector',
							'url_pattern': url_pattern
						}
					});
				}
			}

			//Click handlers
			function initClickSelectors(selectors) {
				selectors.forEach(function(selector) {
					try {
						var selectorElements = b.querySelectorAll(selector.value);
						for(var i = 0; i < selectorElements.length; ++i) {
							selectorElements[i].addEventListener('click', function(e) {
								sendMessage({
									'event': 'user_action',
									'type': 'click',
									'data': {
										'selector': selector.value,
										'_id': selector.name
									}
								});
							});
						}
					} catch(e) {
						sendMessage({
							'event': 'error',
							'type': 'click',
							'data': {
								'message': 'bad query selector',
								'selector': selector.value,
								'_id': selector.name
							}
						});
					}
				});
			}

			clicks_selectors.forEach(function(selector_group) {
					if(checkUrlPattern(selector_group.url_pattern)) {
						initClickSelectors(selector_group.selectors);
					}
			});

			//Views handler
			function initViewSelectors(selectors) {
				var tracking_views = [];
				var saveTrackingTimeout = 1000 * 10;
				selectors.forEach(function(selector) {
					try {
						tracking_views.push({
							selector: selector.value,
							elements: b.querySelectorAll(selector.value),
							showing_time: 0,
							is_hidden: true,
							last_show: 0,
							name: selector.name
						});
					} catch(e) {
						sendMessage({
							'event': 'error',
							'type': 'view',
							'data': {
								'message': 'bad query selector',
								'selector': selector.value,
								'_id': selector.name
							}
						});
					}
				});

				function checkTrackingElements() {
					tracking_views.forEach(function(tracking) {
						var rect = null;
						var rectArea = 0;
						var shownRectArea = 0;
						var is_hidden = false;
						for(var i = 0; i < tracking.elements.length; ++i) {
							rect = tracking.elements[i].getBoundingClientRect();
							rectArea = rect.height * rect.width;
							shownRectArea = Math.max(0, (Math.min(windowX, rect.right) - Math.max(0, rect.left))) * Math.max(0, (Math.min(windowY, rect.bottom) - Math.max(0, rect.top)));
							if(shownRectArea == 0) {
								is_hidden = true;
								break;
							}
						}
						if(is_hidden && !tracking.is_hidden) {
							tracking.showing_time += Date.now() - tracking.last_show;
							tracking.is_hidden = is_hidden;
						} else if(!is_hidden && tracking.is_hidden) {
							tracking.last_show = Date.now();
							tracking.is_hidden = is_hidden;
						}
					});
				}

				function saveTrackingElements() {
					checkTrackingElements();
					tracking_views.forEach(function(tracking) {
						var showing_time = tracking.showing_time;
						if(!tracking.is_hidden) {
							showing_time += Date.now() - tracking.last_show;
						}
						sendMessage({
							'event': 'user_action',
							'type': 'view',
							'data': {
								'selector': tracking.selector,
								'showing_time': showing_time,
								'_id': tracking.name
							}
						});
					});
				}

				checkTrackingElements();
				document.addEventListener('scroll', checkTrackingElements);
				b.addEventListener('onunload', saveTrackingElements);
				setInterval(saveTrackingElements, saveTrackingTimeout);
			}

			views_selectors.forEach(function(selector_group) {
				if(checkUrlPattern(selector_group.url_pattern)) {
					initViewSelectors(selector_group.selectors);
				}
			});
			
	//Scroll handler
	var bodyMaxHeight = b.getBoundingClientRect().height;
	var bodyViewedHeight = windowY + b.getBoundingClientRect().top;
	var timeoutID = null;
	var scrollDelay = 1000 * 5;
	function checkBodyViewedHeight() {
		var newBodyMaxHeight = b.getBoundingClientRect().height;
		var newBodyViewedHeight = windowY - b.getBoundingClientRect().top;
		if(newBodyMaxHeight > bodyMaxHeight || newBodyViewedHeight > bodyViewedHeight) {
			bodyMaxHeight = Math.max(newBodyMaxHeight, bodyMaxHeight);
			bodyViewedHeight = Math.max(newBodyViewedHeight, bodyViewedHeight);
			clearTimeout(timeoutID);
			timeoutID = setTimeout(function () {
				sendMessage({
					'event': 'user_action',
					'type': 'scroll',
					'data': {
						'body_height': bodyMaxHeight,
						'body_viewed': bodyViewedHeight
					}
				});
			}, scrollDelay);
		}
	}
	document.addEventListener('scroll', checkBodyViewedHeight);
	
			//Referrer
			sendMessage({
				'event': 'referrer',
				'type': 'referrer',
				'data': {
					'value': document.referrer
				}
			});
			links.forEach(function(link) {
				var img = document.createElement('img');
				img.src = link;
				iframe.contentDocument.getElementsByTagName('body')[0].appendChild(img);
			});
			
	//Timer
	setInterval(heartBeat, heartBeatTimeout);
	b.addEventListener('onunload', heartBeat);
	
			//User script
			try {
				
			} catch (e) {
				sendMessage({
					'event': 'error',
					'type': 'user_script',
					'data': {
						'message': e.message
					}
				});
			}
			var event_name = 'aidata_7921581';
			var event;
			if(typeof(Event) === 'function') {
				event = new Event(event_name);
			} else {
				event = document.createEvent('Event');
				event.initEvent(event_name, true, true);
			}
			document.dispatchEvent(event);
		};
		onDomReady(function () {
			(function() {
				if (!Event.prototype.preventDefault) {
					Event.prototype.preventDefault=function() {
						this.returnValue=false;
					};
				}
				if (!Event.prototype.stopPropagation) {
					Event.prototype.stopPropagation=function() {
						this.cancelBubble=true;
					};
				}
				if (!Element.prototype.addEventListener) {
					var eventListeners=[];

					var addEventListener=function(type,listener /*, useCapture (will be ignored) */) {
						var self=this;
						var wrapper=function(e) {
							e.target=e.srcElement;
							e.currentTarget=self;
							if (listener.handleEvent) {
								listener.handleEvent(e);
							} else {
								listener.call(self,e);
							}
						};
						if (type=='DOMContentLoaded') {
							var wrapper2=function(e) {
								if (document.readyState=='complete') {
									wrapper(e);
								}
							};
							document.attachEvent('onreadystatechange',wrapper2);
							eventListeners.push({object:this,type:type,listener:listener,wrapper:wrapper2});

							if (document.readyState=='complete') {
								var e=new Event();
								e.srcElement=window;
								wrapper2(e);
							}
						} else {
							this.attachEvent('on'+type,wrapper);
							eventListeners.push({object:this,type:type,listener:listener,wrapper:wrapper});
						}
					};
					var removeEventListener=function(type,listener /*, useCapture (will be ignored) */) {
						var counter=0;
						while (counter<eventListeners.length) {
							var eventListener=eventListeners[counter];
							if (eventListener.object==this && eventListener.type==type && eventListener.listener==listener) {
								if (type=='DOMContentLoaded') {
									this.detachEvent('onreadystatechange',eventListener.wrapper);
								} else {
									this.detachEvent('on'+type,eventListener.wrapper);
								}
								eventListeners.splice(counter, 1);
								break;
							}
							++counter;
						}
					};
					Element.prototype.addEventListener=addEventListener;
					Element.prototype.removeEventListener=removeEventListener;
					if (HTMLDocument) {
						HTMLDocument.prototype.addEventListener=addEventListener;
						HTMLDocument.prototype.removeEventListener=removeEventListener;
					}
					if (Window) {
						Window.prototype.addEventListener=addEventListener;
						Window.prototype.removeEventListener=removeEventListener;
					}
				}
			})();

			document.getElementsByTagName('body')[0].appendChild(iframe);
		});
	})(window, window.document);
	