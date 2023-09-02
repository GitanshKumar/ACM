function load(){
    var container = $("#events");
    $.ajax({
    url: "/events",
    method: "GET",
    data: {"loadmore":true, "count":$(".event").length, "q": document.getElementById("search-bar-events").value},
    success: function(data) {
        var load = document.getElementById("load-more-container");
        $(".outer-container").append(`<div id='spinner' style="width:fit-content;margin:auto;margin-bottom:30px;font-size:16px"><i class='fa fa-spinner fa-spin'></i></div>`);
        load.style.display = "none";
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
        
        document.getElementById("spinner").remove();

        if (data[0]) {
            load.style.display = "block";
        };
    }
})
};

let mybutton = document.getElementById("myBtn");

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}