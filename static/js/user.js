
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




 $(document).ready(function(event){   
   var size=$('#periods option').length; 

    if (size==2){
      $('#periods option').append(' полугодие')
    }
    if (size==4){
      $('#periods option').append(' четверть')
    }
    if (size==3){
      $('#periods option').append(' триместр')
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




    var count_jan=$('table').find('.day01').length;

    if (count_jan){
    $(jan).attr('colspan',count_jan).show()
    }


    var count_feb=$('table').find('.day02').length;
    if (count_feb){
    $(feb).attr('colspan',count_feb).show()
    }

    var count_mar=$('table').find('.day03').length;
    if (count_mar){
    $(march).attr('colspan',count_mar).show()
    }


    var count_ap=$('table').find('.day04').length;
    if (count_ap){
    $(ap).attr('colspan',count_mar).show()
    }

    var count_may=$('table').find('.day03').length;
    if (count_may){
    $(may).attr('colspan',count_may).show()
    }
})







