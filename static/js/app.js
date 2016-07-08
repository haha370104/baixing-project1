'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('staff-system', [
  'ngRoute',
    'ngCookies',
    'ui.router',
    'datatables',
    'loginModule',
    'mainModule',
    'teamModule',
    'departmentModule',
    'changePasswordModule',
    'editProfileModule',
    'editStaffModule'
]);


app.config(function($stateProvider,$urlRouterProvider) {
  $stateProvider
      .state('login',{
        url: '/login',
        views: {
          'main' : {
            templateUrl: '/static/template/login.tpl.html',
            controller: 'LoginCtrl'
          }
        }
      })
      .state('main',{
        url: '/main',
        // abstract: true,
        // templateUrl: 'template/main.tpl.html',
        // controller: "MainCtrl"
        views: {
          'main' : {
            templateUrl: '/static/template/main.tpl.html',
            controller: "MainCtrl"
          }
        }
      })
      .state('main.team',{
        url: '/team',
        views: {
          'team': {
            templateUrl: '/static/template/team.tpl.html',
            controller: 'TeamCtrl'
          }
        }
      })
      .state('main.department',{
        url:'/department',
        views: {
          'department': {
            templateUrl: '/static/template/department.tpl.html',
            controller: 'DepartmentCtrl'
          }
        }
      })
      .state('main.changePassword',{
        url:'/changePassword',
        views: {
          'changePassword': {
            templateUrl: '/static/template/changePassword.tpl.html',
            controller: 'ChangePasswordCtrl'
          }
        }
      })
      .state('main.editProfile',{
        url:'/editProfile',
        views: {
          'editProfile': {
            templateUrl: '/static/template/editProfile.tpl.html',
            controller:'EditProfileCtrl'
          }
        }
      })
      .state('main.editStaff',{
        url:'/editStaff',
        views: {
          'editStaff' : {
            templateUrl: '/static/template/editStaff.tpl.html',
            controller: 'EditStaffCtrl'
          }
        }
      })
  ;
  $urlRouterProvider.otherwise('main');
});
