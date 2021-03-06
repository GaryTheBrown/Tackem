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
                listOfTimers.push(setInterval(obj.updateDrive, 1000, element));
            }.bind(obj));
            listOfTimers.push(setInterval(obj.updateISOS, 1000));

            // $('.trackdata').each(function(index, element) {
            //     $(element).on('click', obj.trackData);
            // }.bind(obj));
        }

        updateDrive(element)
        {
            let id = $(element).data('id');
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/drives/data/${id}`,
                dataType: 'json',
                success: function (result) {
                    let $element = $(`.drivebox[data-id='${result.id}']`);

                    if (result.traylock === true) {
                        $element.find('.drivelock').show();
                    } else {
                        $element.find('.drivelock').hide();
                    }

                    $element.find('.info').html(result.drivestatus);
                    if (result.disc === true) {
                        $element.find('.trackdata').show();
                        if (result.trackdata === false) {
                            $element.find('.trackdata span').show();
                        } else {
                            $element.find('.trackdata span').hide();
                        }
                    } else {
                        $element.find('.trackdata').hide();
                    }

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
                    listOfTimers.forEach(function(timer) {
                        clearInterval(timer);
                    });
                    ShowLoader("CONNECTION LOST");
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
                    let existing = [];
                    $('#isosection').find('.isobox').each(function(index, element) {
                        existing.push($(element).data('name'));
                    }.bind(existing));

                    $('#isocount').html(result.count);
                    result.isos.forEach(function(isoInfo) {

                        let arrayIndex = existing.indexOf(isoInfo.filename);
                        if (arrayIndex === -1) {
                            let newISOclone = $('#isotemplate').children().clone(true);
                            newISOclone.attr('data-name', isoInfo.filename);
                            newISOclone.find('.title').html(isoInfo.filename);
                            $('#isosection').append(newISOclone);
                        } else {
                            existing.splice(arrayIndex, 1);
                        }
                        let $isoElement = $('#isosection').find(`.isobox[data-name="${isoInfo.filename}"]`);
                        $isoElement.find('.info').html(isoInfo.info);

                        if (isoInfo.trackdata === false) {
                            $isoElement.find('.trackdata span').show();
                        } else {
                            $isoElement.find('.trackdata span').hide();
                        }
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
                    }.bind(existing));

                    existing.forEach(function(item) {
                        $('#isosection').find(`.isobox[data-name="${item}"]`).remove();
                    });
                },
                error: function () {
                    listOfTimers.forEach(function(timer) {
                        clearInterval(timer);
                    });
                    ShowLoader("CONNECTION LOST");
                }
            });
        }

        // trackData() {
        //     if ($(this).find("span").is(":hidden")) {
        //         //TODO Add in popup to show the track info
        //     } else {
        //         //TODO Add in popup to create the track info
        //     }
        // }
    }

})();
