(function () {

    $(() => {
        new Discs();
    });

    class Discs
    {
        constructor()
        {
            $("[data-click-action]").each(function(index, element) {
                $(element).on("click", Discs[$(element).data("click-action")]);
            });
        }

        static uploadData()
        {
            let discid = $(this).data("disc-id");
            let $obj = $(this);
            $.ajax({
                type: "POST",
                url: `${APIROOT}ripper/disc/upload/${discid}`,
                dataType: "json",
                success: function (result) {
                    $obj.removeClass("clickable")
                        .removeClass("fa-cloud-upload-alt")
                        .removeAttr("data-action")
                        .removeAttr("data-disc-id")
                        .off("click");
                    if (!result.success){
                        alert(result.error);
                        $obj.addClass("fa-times");
                    } else if (result.uploaded) {
                        $obj.addClass("fa-check");
                    } else {
                        $obj.addClass("fa-times");
                    }
                }
            });
        }

        static searchData()
        {
            let discid = $(this).data("disc-id");
            let $obj = $(this);

            $.ajax({
                type: "GET",
                url: `${APIROOT}ripper/disc/searchapi/${discid}`,
                dataType: "json",
                success: function (result) {
                    $obj.removeClass("clickable")
                        .removeClass("fa-question")
                        .removeAttr("data-action")
                        .removeAttr("data-disc-id")
                        .off("click");
                    if (!result.success) {
                        alert(result.error);
                        $obj.addClass("fa-times");
                    } else if (result.found) {
                        let $parent = $obj.parent().parent();

                        $parent.find("a")
                            .html("View");

                        $parent.find(".fa-time")
                            .removeClass("fa-time")
                            .addClass("fa-check");

                        $parent.find('[data-click-action="uploadData"]')
                            .removeClass("clickable")
                            .removeClass("fa-cloud-upload-alt")
                            .addClass("fa-check")
                            .removeAttr("data-action")
                            .removeAttr("data-disc-id")
                            .off("click");
                        $obj.addClass("fa-check");
                    } else {
                        $obj.addClass("fa-times");
                    }
                }
            });
        }
    }
})();
