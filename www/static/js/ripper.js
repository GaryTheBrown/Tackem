(function () {

    $(() => {
        new Ripper();
    });

    class Ripper
    {
        constructor()
        {
            let obj = this;
            $(".drivebox").each(function(index, element) {
                let driveTimer = setInterval(obj.updateDrive, 1000, element);
            }.bind(obj));
        }

        updateDrive(element)
        {
            let id = $(element).data("id");
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/drives/data/`,
                data: { id: id},
                dataType: 'json',
                success: function (result) {
                    console.log(result);
                    let $element = $(`.drivebox[data-id="${result.id}"]`);

                    if ($element.find('.driveimg').attr('src') != result.traystatus) {
                        $element.find('.driveimg').attr('src', result.traystatus);
                    }
                    if (result.traylock == true) {
                        $element.find('.drivelock').show();
                    } else {
                        $element.find('.drivelock').hide();
                    }

                    $element.find('.info').html(result.drivestatus);

                    let $track = $element.find(".progresstrack .progress-bar");
                    let $total = $element.find(".progresstotal .progress-bar");
                    console.log($track.html());
                    console.log($total.html());
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
            });
        }
    }

})();
