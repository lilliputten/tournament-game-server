/** @module script.js
 *  @since 2022.02.12, 03:34
 *  @changed 2022.02.14, 02:16
 */
/* eslint-disable no-console */

function setName(name) {
  console.log('@:setName', { name });
  makeRequest('/session/set_name/' + name).then(data => {
    console.log('@:set_name_click:set_name', {
      data,
    });
    // debugger;
  });
}

function setNameFromInput() {
  const name_input = $('#name');
  const name = name_input.val();
  console.log('@:setNameFromInput', { name_input, name });
  setName(name);
}

function getName(name) {
  const name_input = $('#name');
  console.log('@:getName', { name, name_input });
  makeRequest('/session/get_name').then(data => {
    const { name } = data;
    console.log('@:get_name_click:get_name', {
      name,
      data,
    });
    // debugger;
    name_input.val(name || '');
  });
}

/// Start app...

$(document).ready(function start() {
  const get_name_button = $('#get_name');
  const set_name_button = $('#set_name');
  const allCookies = document.cookie;
  console.log('@:start', {
    allCookies,
    get_name_button,
    set_name_button,
  });
  set_name_button.on('click', setNameFromInput);
  get_name_button.on('click', getName);
  // getName();
  // testRequest();
});

/// Helper functions...

function makeRequest(requestUrl) {
  // NOTE 2022.02.14, 05:54 -- Js fetch is automatically uses actual cookies and updates it after request.
  // var requestUrl = '/session/start'; // 'hello/test';
  // var sendData = { test: 1 };
  console.log('@:makeRequest:', {
    requestUrl,
    // sendData,
  });
  try {
    return fetch(requestUrl)
      .then(function fetch_success(res, textStatus, jqXHR) {
        var {
          // body,
          status,
          ok,
          headers,
        } = res;
        if (!ok || status !== 200) {
          // TODO: Extend error with request info (url, method, status, reason)
          var errorParams = {
            message: 'Request processing error (' + status + ')',
            url: requestUrl,
            // data: requestDataString,
            // method,
            status,
            reason: 'InvalidResponse',
          };
          const error = new Error('Request processing error (' + status + ')');
          // eslint-disable-next-line no-console
          console.error('@:Requestor:simpleFetch: invalid response', error.message, {
            errorParams,
            error,
            res,
            ok,
            status,
            requestUrl,
            // method,
            // requestDataString,
            // fetchParams,
            headers,
            // params,
            // data,
            // req,
          });
          debugger; // eslint-disable-line no-debugger
          // throw error
          return Promise.reject(error);
        }
        var contentType = headers.get('content-type');
        var isJson = (contentType && contentType.includes('application/json'));
        console.log('@:makeRequest:fetch_success', {
          res,
          textStatus,
          jqXHR,
          contentType,
          isJson,
        });
        // debugger;
        return isJson ? res.json() : res.text();
      })
      .then(function fetch_success_data(data) {
        console.log('@:makeRequest:fetch_success_data', {
          data,
        });
        // debugger;
        return data;
      })
      .catch(function fetch_error(error) {
        console.error('@:makeRequest:fetch_error', {
          error,
        });
        debugger; // eslint-disable-line no-debugger
        return error;
      })
    ;
  }
  catch(error) {
    console.error('@:makeRequest: catched error', {
      error,
    });
    debugger; // eslint-disable-line no-debugger
    return Promise.resolve(error);
  }
}

/// Unused tests...

/* // UNUSED: testRequest
 * function testRequest() {
 *   var requestUrl = '/hello/ccc';
 *   // var sendData = { test: 1 };
 *   console.log('@:testRequest:', requestUrl);
 *   makeRequest(requestUrl)
 *     .then(function fetch_success_data(data) {
 *       console.log('@:testRequest:makeRequest:success', data);
 *       debugger;
 *       return data;
 *     })
 *     .catch(function fetch_error(error) {
 *       console.error('@:testRequest:makeRequest:error', error);
 *       debugger;
 *     })
 *   ;
 * }
 */
/* // UNUSED: testSockets
 * function testSockets() {
 *   NOTE 2022.02.14, 00:57 -- Sockets is unused due to remote-server installation
 *   var socket = io.connect('/');
 *   console.log('@:testSockets', {
 *     io: typeof io,
 *     socket: socket,
 *   });
 *   // this is a callback that triggers when the "message" event is emitted by the server.
 *   socket.on('message', function on_message(data) {
 *     console.log('@:testSockets:on_message', data);
 *     // debugger;
 *   });
 *   socket.on('connect_error', function connect_error(err) {
 *     console.log('@:testSockets:connect_error', err);
 *     // debugger;
 *   });
 *   socket.emit('join', { room: 'my_room' });
 * }
 */
