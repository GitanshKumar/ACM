let searchwait = 0;
function search() {
    $.ajax({
        url: "/search",
        method: "GET",
        data: {
            search: document.getElementById("search-bar").value
        },
        success: function(data) {
            var resultsContainer = $('#results-container');
            resultsContainer.empty();
            if (data.length == 0){
                var a = document.createElement("a");
                a.innerHTML = "No results"
                resultsContainer.append(a)
            }
            else {
                for (var i = 0; i < data.length; i++) {
                    if (data[i].length == 1) {
                        var res = `
                                <a class="res-event" href="/event/${data[i][0]}">
                                    <div>
                                        ${data[i][0]}
                                        <strong style='font-size:12px; margin-left:5px;'>|EVENT|</strong>
                                    </div>
                                </a>
                        `;
                    }
                    else {
                        if (data[i][3] == "MEMBER") {
                            var temp = ` | ${data[i][4]} | ${data[i][3]} | ${data[i][5]} | `;
                        }
                        else {
                            var temp = ` | ${data[i][4]} | `
                        };
                        var res = `
                            <a class="res-profile" href="/profile/${data[i][1]}">
                                <img src="${data[i][2]}">
                                <div>${data[i][0]}<strong>${temp}</strong></div>
                            </a>
                            `;
                    }
                    resultsContainer.append(res);
                }
            }
        },
        error: function(error){
            console.log(`Error ${error}`)
        }
    });
}
function addSpinner() {
    if (!document.getElementById("spinner")){
        $("#results-container").append(`<div id='spinner' style="width:fit-content;margin:auto;"><i class='fa fa-spinner fa-spin'></i></div>`)
    }
}

var searchBar = document.getElementById("search-bar");
var result = document.getElementById("results-container");
searchBar.addEventListener("focus", () => {
    result.style.display = 'block';
    search();
})

searchBar.addEventListener("blur", (event) => {
    const isClickInsideResult = result.contains(event.relatedTarget);
    if (!isClickInsideResult) {
        result.style.display = 'none';
    }
})

searchBar.addEventListener("input", () => {
    addSpinner();
    clearTimeout(searchwait);
    searchwait = setTimeout(search, 300);
    }
);