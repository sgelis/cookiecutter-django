(function ($) {
    "use strict"

    function getRandomStr(length, charset) {
        const characters = charset || "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        const charactersLength = characters.length;
        let result  = "";

        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }

        return result;
    }

    $(document).on("click", ".btn-new-token", function (e) {
        $(e.currentTarget).siblings("input[id*=token]").val(getRandomStr(20))
    });
})(django.jQuery);
