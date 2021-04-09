(function () {

    $(() => {
        new DiscType();
        createEvents();
    });

    function createEvents()
    {

        $("form").submit(function () {

            let this_master = $(this);

            this_master.find('input[type="checkbox"]').each( function () {
                let checkbox_this = $(this);

                if( checkbox_this.is(":checked") == true ) {
                    checkbox_this.attr('value','1');
                } else {
                    checkbox_this.prop('checked',true);
                    checkbox_this.attr('value','0');
                }
            });
            return true;
        });
    }

    class DiscType
    {
        constructor()
        {
            let obj = this;
            $("[data-click-action]").each(function(index, element) {
                $(element).on('click', DiscType[$(element).data("click-action")]);
            });
        }

        static chooseDiscType()
        {
            let discType = $(this).data("disc-type");

            $.ajax({
                type: 'GET',
                url: `${APIROOT}ripper/disc/blank/${discType}`,
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
                    if (r.data.total_results == 0) {
                        $resultslist.html("");
                    } else {
                        r.data.results.forEach(function(result) {
                            let $newClone = $resultTemplate.children().clone(true);
                            $newClone.find("img").attr("src", r.images.secure_base_url + r.images.poster_sizes[2] + result.poster_path);
                            $newClone.find(".discTitle").html(result.title);
                            $newClone.find(".discOriginalTitle").html(result.original_title);
                            $newClone.find(".discOriginalLanguage").html(result.original_language);
                            $newClone.find(".discReleaseDate").html(result.release_date);
                            $newClone.find(".discPopularity").html(result.popularity);
                            $newClone.find(".discOverview").html(result.overview);
                            $newClone.find("input").val("Select " + result.title);
                            $newClone.find("input").attr('data-tmdbid', result.id);
                            $resultslist.append($newClone);
                        });

                        $resultslist.find(".selectMovie").on("click", function(obj) {
                            alert($(this).data("tmdbid"));
                        });
                    }
                },
            });
        }

        static movieSearchIMDBid()
        {
            console.log("Movie Search IMDBid");
        }

        static movieSearchTMDBid()
        {
            console.log("Movie Search TMDBid");
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
