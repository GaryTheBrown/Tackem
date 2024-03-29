(function () {

    $(() => {
        let existingISOs = [];
        let existingConverters = [];
        let timer = setInterval(grabData, 1000);

        $('#isoupload').on('change', function() {
            let file = this.files[0];
            if (confirm(`upload ${file.name}`)) {
                clearInterval(timer);
                ShowLoader("UPLOADING");
                $.ajax({
                    type: 'POST',
                    url: `${APIROOT}ripper/iso/upload`,
                    data: {
                        filename: file.name,
                        filesize: file.size
                    },
                    dataType: 'json',
                    success: function (result) {
                        fetch(result.url, {method:"POST", body:file})
                        .then(response => {
                            if (response.ok) {
                                return response;
                            } else {
                                throw Error(`Server returned ${response.status}: ${response.statusText}`);
                            }
                        })
                        .then(response => {
                            HideLoader();
                            timer = setInterval(grabData, 1000);
                            $(this).val('');
                        })
                        .catch(err => {
                            alert(err);
                            HideLoader();
                            timer = setInterval(grabData, 1000);
                            $(this).val('');
                        });
                    },
                });
            } else {
                $(this).val('');
            }
        });

        function grabData()
        {
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/data`,
                dataType: 'json',
                success: function (result) {
                    if (result.drives) {
                        result.drives.forEach(updateDrive, ripper);
                    }
                    $('#isocount').html(result.isos.length);
                    if (result.isos) {
                        existingISOs = [];
                        $('#isosection').find('.isobox').each(function(index, element) {
                            existingISOs.push($(element).data('name'));
                        });
                        result.isos.forEach(updateISO, ripper);
                        existingISOs.forEach(function(item) {
                            $('#isosection').find(`.isobox[data-name="${item}"]`).remove();
                        });
                    }
                    $('#videoconvertercount').html(result.converters.length);
                    if (result.converters) {
                        existingConverters = [];
                        $('#videoconvertersection').find('.videoconverterbox').each(function(index, element) {
                            existingConverters.push($(element).data('id'));
                        });
                        result.converters.forEach(updateConverter, ripper);
                        existingConverters.forEach(function(item) {
                            $('#videoconvertersection').find(`.videoconverterbox[data-id="${item}"]`).remove();
                        });
                    }
                },
                error: function () {
                    clearInterval(timer);
                    ShowLoader("CONNECTION LOST");
                }
            });
        }

        function updateDrive(drive, index)
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

        function updateISO(iso)
        {
            let arrayIndex = existingISOs.indexOf(iso.filename);
            if (arrayIndex === -1) {
                let $newClone = $('#isotemplate').children().clone(true);
                $newClone.attr('data-name', iso.filename);
                $newClone.find('.title').html(iso.filename);
                $('#isosection').append($newClone);
            } else {
                existingISOs.splice(arrayIndex, 1);
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

        function updateConverter(converter)
        {
            let arrayIndex = existingConverters.indexOf(converter.id);
            if (arrayIndex === -1) {
                let $newClone = $('#videoconvertertemplate').children().clone(true);
                $newClone.attr('data-id', converter.id);
                $newClone.attr('data-disc', converter.discid);
                $newClone.attr('data-track', converter.trackid);
                $newClone.find('.title').html(converter.label);
                $('#videoconvertersection').append($newClone);
            } else {
                existingConverters.splice(arrayIndex, 1);
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

    });
})();
