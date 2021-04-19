(function () {

    $(() => {
        new DiscType();
    });

    class DiscType
    {
        constructor()
        {
            $("[data-click-action]").each(function(index, element) {
                $(element).on("click", DiscType[$(element).data("click-action")]);
            });
            DiscType.watchForComplete();
        }

        static chooseDiscType()
        {
            let discType = $(this).data("disc-type");

            $.ajax({
                type: "GET",
                url: `${APIROOT}ripper/disc/blankdisc/${discType}`,
                dataType: "json",
                success: function (result) {
                    let $section = $("#disctypesection");
                    if (result.disc_html) {
                        $section.html(result.disc_html);
                    }
                    if (result.track_html) {
                        $(".trackripdata").each(function(index, element) {
                            $(element).html(result.track_html);
                        });
                    }
                    $section.find("[data-click-action]").each(function(index, element) {
                        $(element).on("click", DiscType[$(element).data("click-action")]);
                    });
                    $(".trackripdata [data-click-action]").each(function(index, element) {
                        $(element).on("click", DiscType[$(element).data("click-action")]);
                    });
                    DiscType.watchForComplete();
                },
            });
        }

        static chooseTrackType()
        {
            let trackType = $(this).data("track-type");
            let $section = $(this).closest("section");
            let trackId = $section.data("track-id");

            $.ajax({
                type: "GET",
                url: `${APIROOT}ripper/disc/blanktrack/${trackId}/${trackType}`,
                dataType: "json",
                success: function (result) {
                    if (result.track_html) {
                        $section.html(result.track_html);
                    }
                    $section.find("[data-click-action]").each(function(index, element) {
                        $(element).on("click", DiscType[$(element).data("click-action")]);
                    });
                    DiscType.watchForComplete();
                },
            });
        }

        static reselectDisc()
        {
            $.ajax({
                type: "GET",
                url: `${APIROOT}ripper/disc/disctypeselect`,
                dataType: "json",
                success: function (result) {
                    let $section = $("#disctypesection");
                    if (result.disc_html) {
                        $section.html(result.disc_html);
                        $section.find("[data-click-action]").each(function(index, element) {
                            $(element).on("click", DiscType[$(element).data("click-action")]);
                        });
                    }
                    $(".trackripdata").each(function(index, element) {
                        $(element).html("");
                    });
                    DiscType.watchForComplete();
                },
            });
        }

        static reselectTrack()
        {
            let discType = $("#disc_type").val();
            let $section = $(this).closest("section");

            $.ajax({
                type: "GET",
                url: `${APIROOT}ripper/disc/tracktypeselect/${discType}`,
                dataType: "json",
                success: function (result) {
                    if (result.track_html) {
                        $section.html(result.track_html);
                        $section.find("[data-click-action]").each(function(index, element) {
                            $(element).on("click", DiscType[$(element).data("click-action")]);
                        });
                    }
                    DiscType.watchForComplete();
                },
            });
        }

        static movieSearch()
        {
            let name = $("#name").val();
            let year = $("#year").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/searchmovie`,
                data: {
                    name: name,
                    year: year
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.movieShowResults(r.data.results, r.images)){
                        return false;
                    }

                },
            });
        }

        static movieSearchIMDBid()
        {
            let imdbid = $("#imdbid").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/imdbid`,
                data: {
                    imdbid: imdbid
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.movieShowResults(r.data.movie_results, r.images)){
                        return false;
                    }
                },
            });
        }

        static movieSearchTMDBid()
        {
            let tmdbid = $("#tmdbid").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/movietmdbid`,
                data: {
                    tmdbid: tmdbid
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.movieShowResults([r.data], r.images)) {
                        return false;
                    }
                },
            });
        }

        static movieShowResults(results, images)
        {
            let $resultslist = $("#discResults");
            let $resultTemplate = $("#discResultTemplate");
            $resultslist.html("");
            $("#discData").attr('data-images', JSON.stringify(images));

            if (results.length == 0) {
                alert("No Movie Results Found");
            } else if (results.length == 1) {
                DiscType.movieSelectDiscDo(results[0]);
            } else if (results.length > 1) {
                results.forEach(function(result) {
                    let $newClone = $resultTemplate.children().clone(true);
                    DiscType.movieFillInData($discData, result, images);
                    $newClone.find("button").html("Select " + result.title);
                    $newClone.find("button").attr("data-tmdbid", result.id);
                    $newClone.find("button").attr("data-fullInfo", JSON.stringify(result));
                    $resultslist.append($newClone);
                });

                $resultslist.find("[data-click-action]").on("click", function(obj) {
                    alert($(this).data("tmdbid"));
                });
            }
            DiscType.watchForComplete();
        }

        static movieSelectDisc()
        {
            DiscType.movieSelectDiscDo($(this).data("fullInfo"));
        }

        static movieSelectDiscDo(result)
        {
            $("#disc_tmdbid").val(result.id);
            $("#disc_name").val(result.original_title);
            if(result.release_date){
                $("#disc_year").val(result.release_date.split("-")[0]);
            }
            $("#disc_language").val(result.original_language);

            let $discData = $("#discData");
            DiscType.movieFillInData($discData, result, $("#discData").data("images"));
            $discData.show();

            $("#discSearch").hide();
            $("#discResuts").hide();
        }

        static movieFillInData(section, result, images)
        {
            section.find("img").attr("src", images.secure_base_url + images.poster_sizes[2] + result.poster_path);
            section.find(".discTitle").html(result.title);
            section.find(".discOriginalTitle").html(result.original_title);
            section.find(".discOriginalLanguage").html(result.original_language);
            section.find(".discReleaseDate").html(result.release_date);
            section.find(".discPopularity").html(result.popularity);
            section.find(".discOverview").html(result.overview);
        }

        static tvSearch()
        {
            let name = $("#name").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/searchtv`,
                data: {
                    name: name,
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.tvShowResults(r.data.results, r.images)){
                        return false;
                    }

                },
            });
        }

        static tvSearchTVDBid()
        {
            let tvdbid = $("#tvdbid").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/tvdbid`,
                data: {
                    tvdbid: tvdbid
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.tvShowResults(r.data.tv_results, r.images)) {
                        return false;
                    }
                },
            });
        }

        static tvSearchIMDBid()
        {
            let imdbid = $("#imdbid").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/imdbid`,
                data: {
                    imdbid: imdbid
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.tvShowResults(r.data.tv_results, r.images)) {
                        return false;
                    }
                },
            });
        }

        static tvSearchTMDBid()
        {
            let tmdbid = $("#tmdbid").val();

            $.ajax({
                type: "GET",
                url: `${APIROOT}scraper/tvtmdbid`,
                data: {
                    tmdbid: tmdbid
                },
                dataType: "json",
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    if (!DiscType.tvShowResults([r.data], r.images)) {
                        return false;
                    }
                },
            });
        }


        static tvShowResults(results, images)
        {
            let $resultslist = $("#discResults");
            let $resultTemplate = $("#discResultTemplate");
            $resultslist.html("");
            $("#discData").attr('data-images', JSON.stringify(images));
            if (results.length == 0) {
                alert("No TV Show Results Found");
            } else if (results.length == 1) {
                DiscType.tvSelectDiscDo(results[0]);
            } else if (results.length > 1) {
                results.forEach(function(result) {
                    let $newClone = $resultTemplate.children().clone(true);
                    DiscType.tvFillInData($newClone, result, images);
                    $newClone.find("button").html("Select " + result.name);
                    $newClone.find("button").attr("data-tmdbid", result.id);
                    $newClone.find("button").attr("data-click-action", result.id);
                    $newClone.find("button").attr("data-fullInfo", JSON.stringify(result));
                    $resultslist.append($newClone);
                });

                $resultslist.find("[data-click-action]").on("click", function(obj) {
                    alert($(this).data("tmdbid"));
                });
            }
            DiscType.watchForComplete();
        }

        static tvSelectDisc()
        {
            DiscType.tvSelectDiscDo($(this).data("fullInfo"));
        }

        static tvSelectDiscDo(result)
        {
            let $discData = $("#discData");
            $discData.find('input[name="disc_tmdbid"]').val(result.id);
            $discData.find('input[name="disc_name"]').val(result.original_name);
            $discData.find('input[name="disc_language"]').val(result.original_language);

            DiscType.tvFillInData($discData, result, $("#discData").data("images"));
            $discData.show();

            $("#discSearch").hide();
            $("#discResuts").hide();
        }

        static tvFillInData(section, result, images)
        {
            console.log(section.html(), result);
            if (result.poster_path == null) {
                section.find("img").hide();
            } else {
                section.find("img").attr("src", images.secure_base_url + images.poster_sizes[2] + result.poster_path);

            }
            section.find(".discTitle").html(result.name);
            section.find(".discOriginalTitle").html(result.original_name);
            section.find(".discOriginalLanguage").html(result.original_language);
            section.find(".discPopularity").html(result.popularity);
            section.find(".discReleaseDate").html(result.first_air_date);
            section.find(".discOverview").html(result.overview);
        }

        static watchForComplete()
        {
            if ($('[data-click-action="chooseDiscType"], [data-click-action="chooseTrackType"]').length){
                return DiscType.disableComplete();
            }
            return DiscType.enableComplete();
        }


        static disableComplete()
        {
            $("#completeSection").hide();
        }

        static enableComplete()
        {
            $("#completeSection").show();
        }

        static grabFormData()
        {
            let inputs = {};

            $("input").each(function(index, element) {
                let name = $(element).attr("name");
                if (name && name.includes("_")) {
                    inputs[name] = $(element).val();
                }
            });

            return inputs;
        }

        static saveDisc()
        {
            $(this).disabled = true;
            let inputs = DiscType.grabFormData();
            let disc_id = $(this).data("disc-id");
            $.ajax({
                type: "POST",
                url: `${APIROOT}ripper/disc/save/${disc_id}`,
                data: inputs,
                dataType: "json",
                success: function (result) {
                    if (result.lockable) {
                        $("#lockSection").show();
                    }
                    $(this).disabled = false;

                },
            });
        }

        static lockDisc()
        {
            $(this).disabled = true;
            $('[data-click-action="saveDisc"]').disabled = true;
            if(confirm("Are you sure you want to lock this Discs Info?")) {
                let disc_id = $(this).data("disc-id");
                $.ajax({
                    type: "POST",
                    url: `${APIROOT}ripper/disc/lock/${disc_id}`,
                    dataType: "json",
                    success: function (result) {
                        if (result.success) {
                            $("input[type=button]").each(function(index, element){
                                element.remove();
                            });
                            $("input").each(function(index, element){
                                $(element).prop("readonly", true);
                            });
                            $("#lockSection").hide();
                            $("#saveSection").hide();
                        }
                    },
                });
            } else {

            }
        }
    }
})();
