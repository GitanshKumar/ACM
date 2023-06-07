function load(){
    var container = $("#events");
    $.ajax({
    url: "/events",
    method: "GET",
    data: {"loadmore":true, "count":$(".event").length, "q": "{{search}}"},
    success: function(data) {
        if (!data[0]) {
            $("#load-more-container").remove();
        };
        for (var i = 1; i < data.length; i++){
            var event = data[i];
            var tags = "";
            for (var j = 0; j < event[4].length; j++) {
                if (j !== event[4].length - 1) {
                    tags += event[4][j] + ", ";
                } else {
                    tags += event[4][j];
                }
            }
            var innerhtml = `
            <div class="event">
                <div style="margin: 2%;">
                    <a href="/event/${event[0]}" style="color: black;">
                        <h2 class="hov">
                            ${event[0]}
                            <div class="image">
                                <div>
                                    <img src="${event[1]}" style="object-fit: contain;" alt="event poster" width="100%" height="100%">
                                </div>
                            </div>
                        </h2>
                    </a>
                    <div>${event[2]}</div>
                    <p>${event[3]}</p>
                    <div style="font-size: 14px;">${tags}</div>
                </div>
            </div>
            `;
            container.append(innerhtml);
        }
    }
})
};