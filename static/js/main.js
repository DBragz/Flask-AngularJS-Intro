/**
 *
 * @main.js
 * Runs my Main Application.
 *
 * My application takes in a .csv file that contains questions,
 * creates a database and table associated with it.  Following
 * initilization of the question table it then runs a website
 * on local host or 127.0.0.1:5000 in order for the user to 
 * make changesa and pull information from the table.
 * 
 */


 
'use scrict'

// Creates and starts my mainApp application
var mainApp = angular.module('mainApp', [])

// Modifies AngularJS markup so that it works with [[ value ]] instead of {{ value }}.
// This is so that Flask and AngularJS do not evaluate the same expression and have a conflict.
mainApp.config(function($interpolateProvider, $httpProvider){         
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
})