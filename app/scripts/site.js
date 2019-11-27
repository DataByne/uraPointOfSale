/**
 *
 * @file js/site.js
 *
 * Site wide JavaScript
 *
 */

// Extend jQuery with site functions
$.extend({
    /**
     * Get query parameters
     *
     * @returns A dictionary of query parameters
     */
    getParams: function() {
        // Start with an empty dictionary
        var params = {};
        // Get the full URL
        var url = $(location).attr('href');
        // Slice the query parameters from the string and split them apart
        var parameters = url.slice(url.indexOf('?') + 1).split('&');
        for(var i = 0; i < parameters.length; ++i)
        {
          // Add each query parameter to the dictionary
          var param = parameters[i].split('=');
          // URL decode the components of the query parameter
          params[decodeURIComponent(param[0])] = decodeURIComponent(param[1]);
        }
        // Return the dictionary of query parameters
        return params;
    },
    /**
     * Get a query parameter by name
     *
     * @name The name of the query parameter to get
     *
     * @returns The value of the query parameter
     */
    getParam: function(name) {
        return $.getParams()[name];
    },
    /**
     * Get the full URL for the page
     *
     * @returns The full URL for the page
     */
    getFullUrl: function () {
        return $(location).attr('href');
    },
    /**
     * Get the strict URL for the page
     *
     * @returns The strict URL for the page
     */
    getUrl: function () {
        // Get the full URL for the page
        var url = $.getFullUrl();
        // Remove the query parameters if present
        if (url.includes('?')) {
            url = url.slice(0, url.indexOf('?'));
        }
        // Return the strict URL
        return url;
    },
    /**
     * Get the page referrer
     *
     * @returns The page referrer
     */
    getReferrer: function () {
        // Get the page referrer query parameter value
        var referrer = $.getParam('referrer');
        // Return the landing page if the referrer is undefined
        if (referrer === undefined) {
            return '/';
        }
        // return the referrer
        return referrer;
    },
    /**
     * Join an URL by component parts
     *
     * @param base     The base component
     * @param relative The relative component to base
     *
     * @returns The joined URL
     */
    joinUrl: function (base, relative) {
        if (base == undefined) {
            base = '/';
        }
        if (relative == undefined) {
            relative = '';
        }
        if ((base[-1] == '/') || (relative[0] == '/')) {
          return base + relative;
        }
        return base + '/' + relative;
    },
    /**
     * Make a full URL from a strict URL and query parameters
     *
     * @param url        The strict URL
     * @param parameters The query parameters dictionary
     */
    makeUrl: function (url, parameters={}) {
        // Check if there are query parameters
        var params = "";
        if (parameters !== undefined) {
            // Add each query parameter
            $.each(parameters, function (key, value) {
                if (key !== undefined) {
                  // Check if this is the first or an additional parameter
                  if (params == "") {
                      params = '?';
                  } else {
                      params += '&';
                  }
                  // Encode the query parameter key name
                  params += encodeURIComponent(key);
                  // Encode the query parameter value if present
                  if (value !== undefined) {
                      params += '=' + encodeURIComponent(value);
                  }
               }
            });
        }
        /* Return the encoded URL and query parameters */
        return encodeURI(url) + params;
    },
    /**
     * Submit an AJAX form action
     *
     * @param url        The URL to submit the form action
     * @param parameters The query parameters
     * @param method     The method of the query, POST by default
     */
    submitForm: function submitForm(url, parameters=null, method="POST", changeHistory=false) {
        /* Perform an AJAX form action */
        $.ajax({
            // The form action method
            method: method,
            // The form action URL
            url: url,
            // The query parameters
            data: parameters,
            // Successful action
            success: function(data) {
                // Push the history state if needed
                if (changeHistory) {
                    window.history.pushState(null, "", url);
                } else {
                    window.history.replaceState(null, "", url);
                }
                // Open a new HTML document and change the navigation history if needed
                document.open("text/html", changeHistory ? null : "replace");
                // Replace the document
                document.write(data);
                document.close();
            }
        });
    },
    /**
     * Navigate to another page
     *
     * @param url        The URL to navigate
     * @param parameters The query parameters
     * @param method     The method of the query, GET by default
     */
    navigateTo: function (url, parameters=null, method="GET", changeHistory=true) {
        // Navigate to the page through an AJAX query
        $.submitForm(url, parameters, method, changeHistory);
    },
    /**
     * Go back in the history falling back to the landing page
     */
    goBack: function () {
        window.history.back();
    },
    /**
     * Delete the current user
     */
    deleteUser: function (username, url) {
        if (confirm("Are you sure you want to permanatly delete the account and all notes associated with the user '" + username + "'?")) {
            $.navigateTo(url);
        }
    },
    /**
     * Delete a note
     */
     deleteNote: function (title, url) {
        if (confirm("Are you sure you want to permanatly delete the note '" + title + "'?")) {
            $.navigateTo(url);
        }
     },
     /**
      * Delete a reminder
      */
      deleteReminder: function (title, url) {
         if (confirm("Are you sure you want to permanatly delete the reminder '" + title + "'?")) {
             $.navigateTo(url);
         }
      },
    /**
     * Populate a time zone selector
     *
     * @param country    The country code for the time zones
     * @param time_zones The time zone selector to populate
     */
     populateTimeZones: function (country, time_zones) {
        time_zones.attr('disabled', 'disabled');
        time_zones.empty();
        $.getJSON("{{ url_for('gettimezones') }}" + '/' + country, function(data) {
            data.forEach(function(item) {
                time_zones.append($('<option>', { value: item[0], text: item[1] }));
            });
            time_zones.removeAttr('disabled');
        });
    }
});

// On window history popstate
$(window).on('popstate', function (e) {
    $.navigateTo($(location).attr('href'), null, 'GET', false);
});
