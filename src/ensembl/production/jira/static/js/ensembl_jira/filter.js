/*jshint esversion: 6 */

(function ($) {
    "use strict";
    $(document).ready(function () {
        $("#intentions_filter").on("keyup", function () {
            let value = $(this).val().toLowerCase();
            $("#intentions_table > tr").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
    });
})(jQuery || django.jQuery);
