$(document).ready(function () {
  // catch button press event when wanting to leave a community
  $("button#modal").on('click', function (e) {
    var $this = $(this);
    var username = $this.attr("data-username");
    var community_slug = $this.attr("data-community-slug");
    set_leave_community_url(username, community_slug);

    var community_name = $this.attr("data-community-name");
    set_community_name_in_modal(community_name);
  });
});


// set the URL inside the confirmation modal to the community that user wants to leave
function set_leave_community_url(username, community_slug) {
  var url = "/" + community_slug + "/" + username + "/leave/";
  $("a#leave-community").attr("href", url);
}


// set the community name inside the confirmation modal on leaving a community
function set_community_name_in_modal(community_name) {
  $("#modal-community-name").text(community_name);
}
