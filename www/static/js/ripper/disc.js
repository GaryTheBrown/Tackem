(function () {

    $(() => {
        new DiscType();
    });

    class DiscType
    {
        constructor()
        {
            let obj = this;
            $("[data-click-action]").each(function(index, element) {
                $(element).on('click', DiscType[$(element).data("click-action")]);
            });
            DiscType.watchForComplete();
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
            let inputs = [];

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
                type: 'POST',
                url: `${APIROOT}ripper/disc/save/${disc_id}`,
                data: inputs,
                dataType: 'json',
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
                    type: 'POST',
                    url: `${APIROOT}ripper/disc/lock/${disc_id}`,
                    dataType: 'json',
                    success: function (result) {
                        $("input[type=button]").each(function(index, element){
                            element.remove();
                        });
                        $("input").each(function(index, element){
                            $(element).prop("readonly", true);
                        });
                        $("#lockSection").hide();
                        $("#saveSection").hide();
                    },
                });
            } else {

            }

        }

        static chooseDiscType()
        {
            let discType = $(this).data("disc-type");

            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/disc/blankdisc/${discType}`,
                dataType: 'json',
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
                        $(element).on('click', DiscType[$(element).data("click-action")]);
                    });
                    $(".trackripdata [data-click-action]").each(function(index, element) {
                        $(element).on('click', DiscType[$(element).data("click-action")]);
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
                type: 'GET',
                url: `${APIROOT}ripper/disc/blanktrack/${trackId}/${trackType}`,
                dataType: 'json',
                success: function (result) {
                    if (result.track_html) {
                        $section.html(result.track_html);
                    }
                    $section.find("[data-click-action]").each(function(index, element) {
                        $(element).on('click', DiscType[$(element).data("click-action")]);
                    });
                    DiscType.watchForComplete();
                },
            });
        }

        static reselectDisc()
        {
            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/disc/disctypeselect`,
                dataType: 'json',
                success: function (result) {
                    let $section = $("#disctypesection");
                    if (result.disc_html) {
                        $section.html(result.disc_html);
                        $section.find("[data-click-action]").each(function(index, element) {
                            $(element).on('click', DiscType[$(element).data("click-action")]);
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
                type: 'GET',
                url: `${APIROOT}ripper/disc/tracktypeselect/${discType}`,
                dataType: 'json',
                success: function (result) {
                    if (result.track_html) {
                        $section.html(result.track_html);
                        $section.find("[data-click-action]").each(function(index, element) {
                            $(element).on('click', DiscType[$(element).data("click-action")]);
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

            let $resultslist = $("#discResults");
            let $resultTemplate = $("#discResultTemplate");

            $.ajax({
                type: 'GET',
                url: `${APIROOT}scraper/moviesearch`,
                data: {
                    name: name,
                    year: year
                },
                dataType: 'json',
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
                type: 'GET',
                url: `${APIROOT}scraper/moviesearchimdbid`,
                data: {
                    imdbid: imdbid
                },
                dataType: 'json',
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
                type: 'GET',
                url: `${APIROOT}scraper/moviesearchtmdbid`,
                data: {
                    tmdbid: tmdbid
                },
                dataType: 'json',
                success: function (r) {
                    if (!r.success){
                        alert("search Failed");
                        return false;
                    }
                    console.log(r);
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

            // if (results.length == 1) {
                //"select One Here"
            /*} else */ if (results.length >= 1) {
                results.forEach(function(result) {
                    let $newClone = $resultTemplate.children().clone(true);
                    $newClone.find("img").attr("src", images.secure_base_url + images.poster_sizes[2] + result.poster_path);
                    $newClone.find(".discTitle").html(result.title);
                    $newClone.find(".discOriginalTitle").html(result.original_title);
                    $newClone.find(".discOriginalLanguage").html(result.original_language);
                    $newClone.find(".discReleaseDate").html(result.release_date);
                    $newClone.find(".discPopularity").html(result.popularity);
                    $newClone.find(".discOverview").html(result.overview);
                    $newClone.find("button").html("Select " + result.title);
                    $newClone.find("button").attr('data-tmdbid', result.id);
                    $newClone.find("button").attr('data-fullInfo', JSON.stringify(result));
                    $resultslist.append($newClone);
                });

                $resultslist.find("[data-click-action]").on("click", function(obj) {
                    alert($(this).data("tmdbid"));
                });
            }
            DiscType.watchForComplete();
        }


        static tvSearch()
        {
            console.log("TV Show Search");
        }

        static tvSearchTVDBid()
        {
            console.log("TV Show Search TVDBid");
        }

        static tvSearchTMDBid()
        {
            console.log("TV Show Search TMDBid");
        }

        static docSearch()
        {
            console.log("Documentry Search");
        }

        static docSearchIMDBid()
        {
            console.log("Documentry Search IMDBid");
        }

        static docSearchTVDBid()
        {
            console.log("Documentry Search TVDBid");
        }

        static docSearchTMDBid()
        {
            console.log("Documentry Search TMDBid");
        }
    }
})();
