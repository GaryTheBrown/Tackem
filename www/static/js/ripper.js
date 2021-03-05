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
            $('.drivebox').each(function(index, element) {
                listOfTimers.push(setInterval(obj.updateDrive, 1000, element, obj));
            }.bind(obj));
            listOfTimers.push(setInterval(obj.updateISOS, 1000));
        }

        updateDrive(element, obj)
        {
            let id = $(element).data('id');
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/drives/data/${id}`,
                dataType: 'json',
                success: function (result) {
                    let $element = $(`.drivebox[data-id='${result.id}']`);

                    if (result.traylock == true) {
                        $element.find('.drivelock').show();
                    } else {
                        $element.find('.drivelock').hide();
                    }

                    $element.find('.info').html(result.drivestatus);

                    let $track = $element.find('.progresstrack .progress-bar');
                    let $total = $element.find('.progresstotal .progress-bar');
                    if (result.ripping != true) {
                        $track.css('width', result.trackpercent + '%');
                        $track.attr('aria-valuenow', result.trackvalue);
                        $track.attr('aria-valuemax', result.max);
                        $total.css('width', result.totalpercent + '%');
                        $total.attr('aria-valuenow', result.totalvalue);
                        $total.attr('aria-valuemax', result.max);
                        $element.find('.progresstrack .label').html(result.tracklabel);
                        $element.find('.progresstotal .label').html(result.totallabel);
                    } else {
                        $track.css('width', '0%');
                        $track.attr('aria-valuenow', '0');
                        $track.attr('aria-valuemax', '0');
                        $total.css('width', '0%');
                        $total.attr('aria-valuenow', '0');
                        $total.attr('aria-valuemax', '0');
                        $element.find('.progresstrack .label').html('');
                        $element.find('.progresstotal .label').html('');
                    }
                },
                error: function () {
                    listOfTimers.each(function(timer) {
                        clearInterval(timer);
                    });
                }
            });
        }

        updateISOS()
        {
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/iso/data`,
                dataType: 'json',
                success: function (result) {
                    console.log(result);

                    let existing = [];
                    $('#isosection').find('.isobox').each(function(index, element) {
                        existing.push($(element).data('name'));
                    }.bind(existing));

                    $('#isocount').html(result.count);
                    result.isos.each(function(index, isoInfo) {
                        if (!existing.includes(isoInfo.filename)) {
                            let $newISO = $('#isotemplate:first-child').clone();
                            $newISO.attr('data-name', isoInfo.filename);
                            $newISO.find('.title').html(isoInfo.filename);
                            $('#isosection').append($newISO);
                        }
                        //if name in existing update the existing and remove it from the list
                        //if not copy the template and append to isosection
                        let $isoElement = $('#isosection').find(`.isobox[data-name="${isoInfo.filename}"]`);
                        $newISO.find('.info').html(isoInfo.info);
                        let $track = $isoElement.find('.progresstrack .progress-bar');
                        let $total = $isoElement.find('.progresstotal .progress-bar');
                        if (isoInfo.ripping != true) {
                            $track.css('width', isoInfo.trackpercent + '%');
                            $track.attr('aria-valuenow', isoInfo.trackvalue);
                            $track.attr('aria-valuemax', isoInfo.max);
                            $total.css('width', isoInfo.totalpercent + '%');
                            $total.attr('aria-valuenow', isoInfo.totalvalue);
                            $total.attr('aria-valuemax', isoInfo.max);
                            $isoElement.find('.progresstrack .label').html(isoInfo.tracklabel);
                            $isoElement.find('.progresstotal .label').html(isoInfo.totallabel);
                        } else {
                            $track.css('width', '0%');
                            $track.attr('aria-valuenow', '0');
                            $track.attr('aria-valuemax', '0');
                            $total.css('width', '0%');
                            $total.attr('aria-valuenow', '0');
                            $total.attr('aria-valuemax', '0');
                            $isoElement.find('.progresstrack .label').html('');
                            $isoElement.find('.progresstotal .label').html('');
                        }

                        // $('#isosection').find('.isobox[data-name')
                    }.bind(existing));

                },
                error: function () {
                    listOfTimers.each(function(timer) {
                        clearInterval(timer);
                    });
                }
            });
            //TODO This one need to update .isocount and .isosection adding new
            //removing old and some way of showing active and waiting. some mark.
        }
    }

})();
