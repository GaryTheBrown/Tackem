(function () {

    var listOfTimers = [];

    $(() => {
        new Ripper();
    });

    class Ripper
    {
        constructor()
        {
            let obj = this;
            $(".drivebox").each(function(index, element) {
                listOfTimers.push(setInterval(obj.updateDrive, 1000, element, obj));
            }.bind(obj));
        }

        updateDrive(element, obj)
        {
            let id = $(element).data("id");
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/drives/data/${id}`,
                dataType: 'json',
                success: function (result) {
                    let $element = $(`.drivebox[data-id="${result.id}"]`);

                    if (result.traylock == true) {
                        $element.find('.drivelock').show();
                    } else {
                        $element.find('.drivelock').hide();
                    }

                    $element.find('.info').html(result.drivestatus);

                    let $track = $element.find(".progresstrack .progress-bar");
                    let $total = $element.find(".progresstotal .progress-bar");
                    if (result.ripping != true) {
                        $track.css("width", result.trackpercent + "%");
                        $track.attr("aria-valuenow", result.trackvalue);
                        $track.attr("aria-valuemax", result.max);
                        $total.css("width", result.totalpercent + "%");
                        $total.attr("aria-valuenow", result.totalvalue);
                        $total.attr("aria-valuemax", result.max);
                        $element.find(".progresstrack .label").html(result.tracklabel);
                        $element.find(".progresstotal .label").html(result.totallabel);
                    } else {
                        $track.css("width", "0%");
                        $track.attr("aria-valuenow", "0");
                        $track.attr("aria-valuemax", "0");
                        $total.css("width", "0%");
                        $total.attr("aria-valuenow", "0");
                        $total.attr("aria-valuemax", "0");
                        $element.find(".progresstrack .label").html("");
                        $element.find(".progresstotal .label").html("");
                    }
                },
                error: function () {
                    listOfTimers.forEach(function(timer) {
                        clearInterval(timer);
                    });
                }
            });
        }

        updateISOS(obj)
        {
            //TODO This one need to update .isocount and .isosection adding new
            //removing old and some way of showing active and waiting. some mark.
        }
    }

})();
