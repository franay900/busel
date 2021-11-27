
function take_off(one,two,three){
	$('input[type="date"]').val('')
	$('#one_title').text(one)
	$('#two_title').text(two)
	$('#three_title').text(three)
}

function radio(){

	$('#four').click(function(){
		take_off('1 четверть','2 четверть','3 четверть')
		$('#three_per').removeClass("d-none")
		$('#four_per').removeClass("d-none")
	
	});
$('#three').click(function(){
	take_off('1 триместр','2 триместр','3 триместр')
	$('#four_per').addClass("d-none")
	$('#three_per').removeClass("d-none")
});
$('#two').click(function(){
	take_off('1 полугодие','2 полугодие')
	$('#three_per').addClass("d-none")
	$('#four_per').addClass("d-none")
	
});




}

function save_mark(self,url,tocken,min,max){
    
    $(self).css('display','none')
    var old_mark=$(self).attr('old_mark')
    var new_mark=$(self).val()
    var attendance=0
    if ((new_mark>=min & new_mark<=max ) | (old_mark!='' & new_mark=='') | new_mark=='н' | new_mark=='н/а' ){
      
	    var td_id=$(self).attr('td')
      var student=$('#'+td_id).attr('student')
      var type=0
      var lesson=0
      var red_mark=0
      var del_mark=0
      var itog=0
      var isitog=0
      if ($('#'+td_id).attr('type')){
        type=$('#'+td_id).attr('type')
        
        lesson=$('#'+td_id).attr('lesson')
      }
      if($('#'+td_id).attr('period')){
        itog=$('#'+td_id).attr('period')
        lesson=$('#'+td_id).attr('load')
      }
      if($('#'+td_id).attr('itog')){
        itog=1
        lesson=$('#'+td_id).attr('load')
        isitog=$('#'+td_id).attr('itog')
      }
	    $('#'+td_id).text(new_mark)
      
      
      if (old_mark!=new_mark & old_mark!='' & new_mark!='' ){
        red_mark=$('#'+td_id).attr('markpk')
      }
      if (old_mark!='' & new_mark=='' ){

        del_mark=$('#'+td_id).attr('markpk')
      }
      if(new_mark=='н'){
        new_mark=0
        attendance=1
      }
      if(new_mark=='н/а'){
        new_mark=0
        attendance=1
      }
	    $.ajax({

		  url: url,
		  method: 'post',
		  dataType: 'html',
		  data: {
        isitog:isitog,
        itog:itog,
        attendance:attendance,
        red_mark:red_mark,
        del_mark:del_mark,
  			mark: new_mark,
        student:student,
        type:type,
        lesson:lesson,
  			csrfmiddlewaretoken: tocken
		  },

  		  success: function(data){

  			var student=$('#'+td_id).attr('student')
        var marks=$('.'+student)
        var mark_sum=0
        var mark_lenght=0
        $('.'+student).each(function(){
           var mark=$(this).text()
           
           if (mark>=1 & mark<=100){
              mark_sum=mark_sum+parseInt(mark)
              mark_lenght=mark_lenght+1
           }
        });
        var ball=mark_sum/mark_lenght
        ball=ball.toFixed(2)
        if (ball>0){
        $('#ball'+student).text(ball)
      }
        else{
          $('#ball'+student).text('')
        }
        $('#'+td_id).attr('markpk',data)
  		}
	});
}
}



function click_mark(self){

  var td=$(self)
  var td_id=td.attr('id')
  var old_mark=$(self).html()

  var dayTop=$(self).offset().top
  var dayLeft=$(self).offset().left
  var dayWidth=$(self).css('width')
  var dayHeight=$(self).css('height')
  var mark=$("#mark")

  mark.val(old_mark)
  mark.css({'display':'block','width':dayWidth,'height':dayHeight}).offset({'top':dayTop,'left':dayLeft}).focus()

  mark.attr({'old_mark':old_mark,'td':td_id})
  
}


 $(document).ready(function(event){   
   var size=$('#periods option').length; 

    if (size==2){
      $('#periods option').append(' полугодие')
    }
    if (size==4){
      $('#periods option').append(' четверть')
    }
    $('#scroll').scrollLeft(9999)

    var month=$('.month').css('height')
    var month=parseInt(month)*3
    $('#row-2').css('height',month)

    $('#nrow-2').css('height',month)
    
    var count_sep=$('table').find('.day09').length;
    if (count_sep){
      $(sep).attr('colspan',count_sep).show()
  }
    var count_oct=$('table').find('.day10').length;
    if (count_oct){
    $(oct).attr('colspan',count_oct).show()
  }
    var count_nov=$('table').find('.day11').length;
    if (count_nov){
      $(nov).attr('colspan',count_nov).show()
    }
    var count_dec=$('table').find('.day12').length;
    if (count_dec){
    $(dec).attr('colspan',count_dec).show()
    }

})