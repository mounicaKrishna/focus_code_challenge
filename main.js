$(function (){
    var $searchques = $('#search-ques')
    var $answers = $('#answers')
    var $updateques = $('#update-ques')
    var $answer1 = $('#update-ans1')
    var $answer2 = $('#update-ans2')
    var $answer3 = $('#update-ans3')

    $.ajax({
    type: 'GET',
    url: 'http://localhost:8080/port',
    success: function(orders) {
    $.each(orders, function(i,order) {
        console.log('success', orders)
    });
    }
    });

    $('#search-button').on('click', function(){
        var search_json = {
            question: $('#search-ques').val()
        };

    $.ajax({
    type: 'POST',
    url: 'http://localhost:8080/search-question',
    data: JSON.stringify(search_json),
    dataType:"json",

    success: function(answers){

    $.each(answers, function(i,answer) {
        $answers.append('<li> '+ answer)

    });
    },
    error: function(){
     alert("error while searching for question")}
    }
    )
    })



//Update
    $('#update-button').on('click', function(){
        var update_json = {
            question: $('#update-ques').val(),
            answer1: $('#update-ans1').val(),
            answer2: $('#update-ans2').val(),
            answer3: $('#update-ans3').val()
        };
    console.log("update_json", update_json)
    $.ajax({
    type: 'POST',
    url: 'http://localhost:8080/update-question',
    data: JSON.stringify(update_json),
    dataType:"json",

    success: function(){
      alert("Your questions have been updated")
    },
    error: function(){
     alert("error while updating the question")}
    }
    )
    })

});