/*jslint node:true */
"use strict";

var child_process = require('child_process');

var env = (process.env.NODE_ENV === 'production') ? 'production' : 'development';

// List of client side javascript libraries
var lib_js_list = [
    'static/js/libs/angular/angular.min.js'
];

// List of tic-tac-toe javascript files
var tictactoe_js_list = [
    'static/js/controllers/*.js'
];

var gruntConfig = {
    pkg: require('./package.json'),

    jshint: {
        options: {
            curly: true,
            laxbreak: true,
            es3: true,
            eqnull: true,
            browser: true,
            jquery: true
        },
        tictactoe_js: {
            files: [tictactoe_js_list]
        }
    },

    uglify: {
        development: {
            options: {
                mangle: false,
                preserveComments: 'all',
                compress: false,
                beautify: true
            },
            files: {
                'static/js/tictactoe.dev.js': [lib_js_list, tictactoe_js_list]
            }
        },
        production: {
            options: {
                mangle: true,
                preserveComments: false,
                compress: {
                    unused: false
                }
            },
            files: {
                'static/js/tictactoe.min.js': [lib_js_list, tictactoe_js_list]
            }
        }
    }
};

// Keep just the right ENV
delete gruntConfig.uglify[env === 'production' ? 'development' : 'production'];

module.exports = function(grunt) {
    // Project configuration
    grunt.initConfig(gruntConfig);

    // Load the plugins
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Default task(s)
    grunt.registerTask('build', ['uglify']);
};