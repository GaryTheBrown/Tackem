(function () {

    $(() => {
        new Ripper();
    });

    class Ripper
    {
        constructor()
        {
            this.existingISOs = [];
            this.existingConverters = [];

            if (window.location.href.endsWith("/ripper/")){
                this.timer = setInterval(this.grabData.bind(this), 1000);
            }

            // $('.trackdata').each(function(index, element) {
            //     $(element).on('click', obj.trackData);
            // }.bind(obj));
        }

        grabData()
        {
            var ripper = this;
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/data/`,
                dataType: 'json',
                success: function (result) {
                    if (result.drives) {
                        //loop through drives and update them
                        result.drives.forEach(ripper.updateDrive, ripper);
                    }
                    $('#isocount').html(result.isos.length);
                    if (result.isos) {
                        //Grab the existing ISOs shown as a list of names
                        ripper.existingISOs = [];
                        $('#isosection').find('.isobox').each(function(index, element) {
                            ripper.existingISOs.push($(element).data('name'));
                        }.bind(ripper));

                        //loop through isos and update them
                        result.isos.forEach(ripper.updateISO, ripper);

                        //Remove unlisted isos
                        ripper.existingISOs.forEach(function(item) {
                            $('#isosection').find(`.isobox[data-name="${item}"]`).remove();
                        });
                    }
                    $('#videoconvertercount').html(result.converters.length);
                    if (result.converters) {
                        //Grab the existing Converters shown as a list of ids
                        ripper.existingConverters = [];
                        $('#videoconvertersection').find('.videoconverterbox').each(function(index, element) {
                            ripper.existingConverters.push($(element).data('id'));
                        }.bind(ripper));

                        //loop through Converters and update them
                        result.converters.forEach(ripper.updateConverter, ripper);

                        //Remove unlisted Converters
                        ripper.existingConverters.forEach(function(item) {
                            $('#videoconvertersection').find(`.videoconverterbox[data-id="${item}"]`).remove();
                        });
                    }
                },
                error: function () {
                    clearInterval(ripper.timer);
                    ShowLoader("CONNECTION LOST");
                }
            });
        }

        updateDrive(drive, index)
        {
            let $element = $(`.drivebox[data-id='${index}']`);

            if (drive.traylock === true) {
                $element.find('.drivelock').show();
            } else {
                $element.find('.drivelock').hide();
            }

            $element.find('.info').html(drive.drivestatus);
            if (drive.disc === true) {
                $element.find('.trackdata').show();
                if (drive.trackdata === false) {
                    $element.find('.trackdata span').show();
                } else {
                    $element.find('.trackdata span').hide();
                }
            } else {
                $element.find('.trackdata').hide();
            }

            let $track = $element.find('.progresstrack .progress-bar');
            let $total = $element.find('.progresstotal .progress-bar');
            if (drive.ripping != true) {
                $track.css('width', drive.trackpercent + '%');
                $track.attr('aria-valuenow', drive.trackvalue);
                $track.attr('aria-valuemax', drive.max);
                $total.css('width', drive.totalpercent + '%');
                $total.attr('aria-valuenow', drive.totalvalue);
                $total.attr('aria-valuemax', drive.max);
                $element.find('.progresstrack .label').html(drive.tracklabel);
                $element.find('.progresstotal .label').html(drive.totallabel);
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
        }

        updateISO(iso)
        {
            let arrayIndex = this.existingISOs.indexOf(iso.filename);
            if (arrayIndex === -1) {
                let newISOclone = $('#isotemplate').children().clone(true);
                newISOclone.attr('data-name', iso.filename);
                newISOclone.find('.title').html(iso.filename);
                $('#isosection').append(newISOclone);
            } else {
                this.existingISOs.splice(arrayIndex, 1);
            }
            let $isoElement = $('#isosection').find(`.isobox[data-name="${iso.filename}"]`);
            $isoElement.find('.info').html(iso.info);

            if (iso.trackdata === false) {
                $isoElement.find('.trackdata span').show();
            } else {
                $isoElement.find('.trackdata span').hide();
            }
            let $track = $isoElement.find('.progresstrack .progress-bar');
            let $total = $isoElement.find('.progresstotal .progress-bar');
            if (iso.ripping != true) {
                $track.css('width', iso.trackpercent + '%');
                $track.attr('aria-valuenow', iso.trackvalue);
                $track.attr('aria-valuemax', iso.max);
                $total.css('width', iso.totalpercent + '%');
                $total.attr('aria-valuenow', iso.totalvalue);
                $total.attr('aria-valuemax', iso.max);
                $isoElement.find('.progresstrack .label').html(iso.tracklabel);
                $isoElement.find('.progresstotal .label').html(iso.totallabel);
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
        }

        updateConverter(converter)
        {
            let arrayIndex = this.existingConverters.indexOf(converter.id);
            if (arrayIndex === -1) {
                let newISOclone = $('#videoconvertertemplate').children().clone(true);
                newISOclone.attr('data-id', converter.id);
                newISOclone.attr('data-disc', converter.discid);
                newISOclone.attr('data-track', converter.trackid);
                newISOclone.find('.title').html(converter.label);
                $('#videoconvertersection').append(newISOclone);
            } else {
                this.existingConverters.splice(arrayIndex, 1);
            }
            let $videoconverterElement = $('#videoconvertersection').find(`.videoconverterbox[data-id="${converter.id}"]`);

            let $track = $videoconverterElement.find('.progress-bar');
            if (converter.converting == true) {
                $videoconverterElement.find('.info').html("Converting");
                $track.css('width', converter.percent + '%');
                $track.attr('aria-valuenow', converter.process);
                $track.attr('aria-valuemax', converter.framecount);
                $videoconverterElement.find(' .label').html(`${converter.process}/${converter.framecount} (${converter.percent}%)`);
            } else {
                $videoconverterElement.find('.info').html("Waiting For Free Converter");
                $track.css('width', '0%');
                $track.attr('aria-valuenow', '0');
                $track.attr('aria-valuemax', '0');
                $videoconverterElement.find('.label').html('');
            }
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
