function load(){
    var container = $(".search-results");
    $.ajax({
    url: "/search",
    method: "GET",
    data: {"loadmore":true, "count":$(".result").length, "q": document.getElementById("search-bar").value},
    success: function(data) {
        if (!data[0]){
            $("#load-more-container").remove();
        }
        document.getElementById("count").innerText = `Showing ${data[1]} out of ${data[2]} results for ${document.getElementById("search-bar").value}`
        for (var i = 3; i < data.length; i++){
            var res = data[i];
            if (res[0] == "event"){
                var tags = "";
                for (var j = 0; j < res[5].length; j++) {
                    if (j !== res[5].length - 1) {
                        tags += res[5][j] + ", ";
                    } else {
                        tags += res[5][j];
                    }
                };
                var innerhtml = `
                <div class="result">
                    <div style="margin: 2%;">
                        <a href="/event/${res[1]}/" style="color: black;">
                            <h2 class="hov">
                                ${res[1]}
                                <div class="image">
                                    <div>
                                        <img src="${res[2]}" style="object-fit: contain;" alt="event poster" width="100%" height="100%">
                                    </div>
                                </div>
                            </h2>
                        </a>
                        <div>${res[3]}</div>
                        <p>${res[4]}</p>
                        <div style="font-size: 14px;">${tags}</div>
                    </div>
                </div>
                `;
                container.append(innerhtml);
            }
            else {
                var innerhtml = `
                <div class="result">
                    <div style="margin: 2%;">
                        <div style="display: flex;">
                            <a href="/profile/${res[2]}" style="color: black;">
                                <img src="${res[3]}" width="100xpx" style="border-radius: 50%; border: 1px solid rgba(0,0,0,0.2);">
                            </a>
                            <div style="padding-left: 15px;padding-right: 15px; border-right: 1px solid rgba(0,0,0,0.2);">
                                <h2 style="margin: 0;">${res[1]}</h2>
                                <div style="margin-bottom: 5px;">${res[4]} ${res[5]} year</div>
                            </div>
                            <div style="padding-left: 15px;">
                                <p style="margin-top: 0;">${res[7]}</p>
                            </div>
                        </div>
                    </div>
                </div>
                `
                container.append(innerhtml);
            }
        }
    }
})
}