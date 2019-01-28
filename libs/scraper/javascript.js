function ClearModel(){
	$('#search_modal').find(".modal-title").html("");
	$('#search_modal').find(".modal-body").html("");
	$('#search_modal').find(".modal-footer").html("");
	$('#search_modal').modal('hide');
}

function FillModel(item){
	if (item['success']){
		$('#search_modal').find(".modal-title").html(item['header']);
		$('#search_modal').find(".modal-body").html(item['body']);
		$('#search_modal').find(".modal-footer").html(item['footer']);
		$('#search_modal').modal('show');
	}else{
		console.log("ERROR:" + item['status'] + ":" + item['reason']);
	}
}

function CallAJAX(url){
	$.ajax(url, {
		success: function(jsonitem) {
			var item = JSON.parse(jsonitem)
			FillModel(item);
		}
	})
}

function SearchMovie(query, year=null, page=1){
	url = '%%BASEURL%%scraper/searchmovie/' + query + '/' + page + '/'
	if (year != null) url += year + '/';
	CallAJAX(url);
}

function ButtonSearchMovie(){
	name = $('#disctypesection').find('input[name="name"]').val()
	year = $('#disctypesection').find('input[name="year"]').val()
	if (year == "") year = null;
	if (name != ""){
		SearchMovie(name, year, 1);
	}
}

function ButtonFindMovie(){
	imdbid = $('#disctypesection').find('input[name="imdbid"]').val()
	if (imdbid != ""){
		CallAJAX('%%BASEURL%%scraper/findmovie/' + imdbid + '/');
	}
}

function PopulateMovie(id){
	///will use the data in the modal and populate the movie info on the main page
	console.log(id);
}
