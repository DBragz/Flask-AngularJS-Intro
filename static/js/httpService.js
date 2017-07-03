/**
 * @httpService
 * Module that is used in order to make 
 * http calls.
 *
 * This module is able to creates POST,
 * GET, and DELETE http calls.
 * 
 */
 
// Creates the httpService module
mainApp.factory('httpService', function($http, $q) {
   
   'use scrict'
    
   // Allows who ever has access to this module to 
   // call the following functions.
   return ({
        
        getRequest: getRequest,
        postRequest: postRequest,
        deleteRequest: deleteRequest
        
   });
   
  /**
   * Creates a GET request from a server
   *
   * @param {string} url
   *   The url server address to try and access 
   *   or send information to.
   * @param {object} data
   *   The object being used to pass to the server.
   * @param {function} returnFunc
   *   The function to return to after http call.
   *
   * @return {request} request
   *    Returns the response from the 
   *    server to the return function.
   * 
   */
   
   function getRequest(url, data, returnFunc) {
           
        var request = $http({
                    method: 'get',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    url: url,
                    params: data
                    
                });

        return( request.then( returnFunc, returnFunc ) );

   }
   
  /**
   * Creates a POST request from a server
   *
   * @param {string} url
   *   The url server address to try and access 
   *   or send information to.
   * @param {object} data
   *   The object being used to pass to the server.
   * @param {function} returnFunc
   *   The function to return to after http call.
   *
   * @return {request} request
   *    Returns the response from the 
   *    server to the return function.
   * 
   */
   
   function postRequest(url, data, returnFunc) {
           
           var request = $http({
                    method: 'post',
                    url: url,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    params: data
                });
           
           return( request.then( returnFunc, returnFunc ) );
       
   } 
   
  /**
   * Creates a DELETE request from a server
   *
   * @param {string} url
   *   The url server address to try and access 
   *   or send information to.
   * @param {object} data
   *   The object being used to pass to the server.
   * @param {function} returnFunc
   *   The function to return to after http call.
   *
   * @return {request} request
   *    Returns the response from the 
   *    server to the return function.
   * 
   */
   
   function deleteRequest(url, data, returnFunc) {
           
           var request = $http({
                    method: 'delete',
                    url: url,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    params: data
                });
           
           return( request.then( returnFunc, returnFunc ) );
       
   } 
   
   
});