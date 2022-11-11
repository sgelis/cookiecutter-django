/* Adapted from admin/js/jquery.init.js.
 *
 * Registers jQuery on both django.jQuery **and** the usual $.
 */
(function () {
    window.django = window.django || {};
    window.django.jQuery = jQuery.noConflict(false);
    window.$ = jQuery.noConflict(false);
})();
