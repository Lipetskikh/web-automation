(function () {
	// === 1. console monitoring ===
	const originalConsole = {
		error: console.error,
		warn: console.warn,
		log: console.log,
		group: console.group,
		groupCollapsed: console.groupCollapsed,
		table: console.table
	};
	
	let consoleGraphQLErrorLogged = false; // flag that error was printed in console
	const consoleErrorMessages = []; // original messages in Console
	let lastGraphQLErrorTime = 0;
	const WATCH_WINDOW_MS = 5000;
	let lastErrorMessages = [];
	let isSnippetLogging = false;
	
	
	function checkConsoleArgs(args, method) {
		if (isSnippetLogging){
			return;
		}
		
		const text = Array.from(args).map(a => {
			try {
				return typeof a === 'string' ? a : JSON.stringify(a);
				} catch (e) {
					return String(a);
					}
		}).join(' ');
		const now = Date.now();
		const isInsideWatchWindow = (now - lastGraphQLErrorTime) < WATCH_WINDOW_MS;
		// typical patterns
		const isSpecificGraphQL = 
			/\[GraphQL error\]/i.test(text) ||
			/graphQLErrors/i.test(text) ||
			/GraphQL error/i.test(text) ||
			/AppolloError/i.test(text) ||
			/Network error.*graphql/i.test(text) ||
			(text.includes('errors') && text.includes('message') && text.includes('path'));
		
		// errors (text) from message
		const containsErrorMessage = lastErrorMessages.some(msg => {
			if (!msg || msg.length < 10) { // if too short message
				return false;
			}
			return text.includes(msg);
		})
		
		// other error/warn in temporal window
		const isGenericInWindow = 
			isInsideWatchWindow &&
			(method === 'error' || method === 'warn') &&
			text.trim().length > 0;
		
		if (isSpecificGraphQL || containsErrorMessage || isGenericInWindow) {
			//consoleGraphQLErrorLogged = true;
			//consoleErrorMessages.push(`[${method}] ${text.slice(0, 300)}`);
			consoleErrorMessages.push(text.slice(0, 500));
		}
	}
	
	['error', 'warn', 'log', 'group', 'groupCollapsed', 'table'].forEach(method => {
		console[method] = function(...args) {
			checkConsoleArgs(args);
			return originalConsole[method].apply(console, args);
		};
	});
	
	function snippetLog(fn) {
		isSnippetLogging = true;
		try {
			fn();
		} finally {
			isSnippetLogging = false;
		}
	}
	
	// === 2. take fetch (find errors in responses) ===
	const originalFetch = window.fetch;
	const foundErrors = [];
	
	window.fetch = async function (...args) { 
		const response = await originalFetch.apply(this, args);
		const url = (args[0] && args[0].url) || String(args[0] || '');
		// take only json
		const ct = response.headers.get('content-type') || ''; 
		if (!ct.includes('application/json') && !ct.includes('application/graphql')) { // skip not-json
			return response;
		}
		
		try {
			const clone = response.clone();
			const body = await clone.json();
			
			// batch-answeres (array) and single
			const payloads = Array.isArray(body) ? body : [body];
			
			payloads.forEach((payload, idx) => {
				if (!payload || typeof payload !== 'object') {
					return;
				}
				
				// main attribute of GraphQL-response
				const hasErrors = Array.isArray(payload.errors) && payload.errors.length > 0;
				const hasData = Object.prototype.hasOwnProperty.call(payload, 'data');
				if (!hasErrors) {
					return;
				}
				// save all message from errors
				lastErrorMessages = payload.errors.map(e => e.message).filter(Boolean);
				lastGraphQLErrorTime = Date.now();
				
				const bodyStatus = 
					payload.errors?.[0]?.extensions?.originalError?.statusCode ??
					payload.errors?.[0]?.extensions?.code ??
					response.status;
				
				const entry = {
					url,
					status: bodyStatus,
					httpStatus: response.status,
					batchIndex: Array.isArray(body) ? idx : null,
					errors: payload.errors,
					hasData: !!payload.data,
					timestamp: new Date().toISOString(),
					loggedByApp: false
				};
				foundErrors.push(entry);
				
				setTimeout(() => {
					const logged = consoleErrorMessages.some(log =>
						lastErrorMessages.some(msg => log.includes(msg))
						);
					entry.loggedByApp = logged;
					
					if (!logged) {
						snippetLog(() => {
							console.group('%cGraphQL ERROR not logged by application!', 'color:white;background:#d32f2f;font-weight:bold;font-size:14px;padding:4px 8px;border-radius:3px;');
							console.log('URL: ', url);
							console.log('Status from body: ', bodyStatus);
							console.log('HTTP status: ', response.status);
							console.table(
								payload.errors.map(e => ({
								message: e.message,
								path: Array.isArray(e.path) ? e.path.join('.') : e.path,
								code: e.extensions?.originalError?.statusCode
								}))
							);
							console.log('Full payload: ', payload);
							console.groupEnd();
						});
					}
				}, 700);
			});
		} catch (_) {
			// not json or aborted => skip
		}
		
		return response;
	};
	// === 3. Functions for hand-check ===
	window.__gqlCheck = {
		// show all found network-errors
		list() {
			console.table(foundErrors.map(e => ({
				url: e.url,
				status: e.status,
				loggedByApp: e.loggedByApp ? 'YES' : 'NO',
				errorsCount: e.errors?.length,
				//hasData: e.hasData,
				time: e.timestamp,
			})));
			return foundErrors;
		},
		// main report: network-errors + messages in Console (if it was)
		report() {
			const logged = foundErrors.filter(e => e.loggedByApp);
			const notLogged = foundErrors.filter(e => !e.loggedByApp);
			
			snippetLog(() => {
				console.group('%cGraphQL Errors Report', 'font-weight:bold;font-size:14px');
				console.log('Total GraphQL errors in network:', foundErrors.length);
				console.log('Network responses with errors: ', foundErrors.length);
				console.log('%cLogged by application:', 'color:green; fontweight:bold', logged.length);
				console.log('%cNOT logged by application:', 'color:#d32f2f;fontweight:bold', notLogged.length);

				if (notLogged.length > 0) {
					console.log('\nErrors that were NOT logged by the application:');
					console.table(foundErrors.map(e => ({
						url: e.url.slice(-80),
						status: e.status,
						messages: e.errors.map(er => er.message).join(' | '),
				})));
			}
			
			if (logged.length > 0) {
				console.log('\n(Logged errors are shown above in Console in the form written by developers)');
			}
			console.groupEnd();
			});
			
			return {
				total: foundErrors.length,
				loggedByApp: logged.length,
				notLoggedByApp: notLogged.length,
				details: foundErrors,
			};
		},
		// refresh counters
		reset() {
			foundErrors.length = 0;
			//consoleGraphQLErrorLogged = false;
			consoleErrorMessages.length = 0;
			lastGraphQLErrorTime = 0;
			lastErrorMessages = [];
			console.log('Couners refreshed');
		},
	};
	
	console.log('%cGraphQL error interceptor active (by response structure, not by URL)', 'color:green;font-weight:bold');
	console.log('Commands: __gqlCheck.report() | __gqlCheck.list() | __gqlCheck.reset()');
})();