



jQuery(document).ready(function(){




$('.btn-tooltip').tooltip();
$("[data-toggle=popover]").popover();   

  $('.mark_tr').each(function(){

           var mark_sum=0
           var mark_lenght=0
           var mark=$(this).children('td').text()
           var student=$(this).children('td').attr('student')
           for (i = 0; i < mark.length; i +=1 ) {
              if(parseInt(mark[i])>0){
              mark_sum=mark_sum+parseInt(mark[i])
              mark_lenght+=1
            }
          }
           var ball=mark_sum/mark_lenght
           
           ball=ball.toFixed(2)
           
           if(ball>0){
              $('#ball'+student).text(ball)
         }


         
  });

    if($('#month').text()==3){
        $('#month').text('Март');
  }


    if($('#month').text()==4){
        $('#month').text('Апрель');
  }


    if($('#month').text()==5){
        $('#month').text('Май');
  }


    $('.disabled_date').on('click',function(event){
      $('#liveToast2').toast('show');
  })




$('.date1').click(function(){
  if ($('#notice').attr('status')=='enable'){
  var top_this=$(this).offset().top
  var left_this=$(this).offset().left
  var block=$('.block')
  $('.day').attr('checked',false)
  $(block).attr('tdid',$(this).attr('id'))
  $('.block').css('display','block')
  $('.block').offset({ top: top_this+25, left: left_this});
  
  $('#days').empty()
  $('.close_button').attr('student_pk',$(this).attr('student_pk'))

  $.ajax({
  url: $('.block').attr('url'),         /* Куда пойдет запрос */
  method: 'get',             /* Метод передачи (post или get) */
  dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
  data: {date: $(this).attr('date_at'), month:$('.block').attr('month_at'), year:$('.block').attr('year_at'), class:$('.block').attr('class_pk'), student: $(this).attr('student_pk')},     /* Параметры передаваемые в запросе. */
  success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
      var lessons=data.lessons;            /* В переменной data содержится ответ от index.php. */
      var pks=data.pks;  
      var marks=data.marks
      
      for (i = 0; i < lessons.length; i +=1 ) {

        
        var day=$('#days').append(' <div class="custom-control custom-checkbox " id="ex_lesson"><input type="checkbox" class="custom-control-input" id="'+pks[i]+'"><label class="custom-control-label" for="'+pks[i]+'">'+lessons[i]+'</label></div>')
        $(day).attr('day_pk',pks[i])

        if ($.inArray( pks[i], marks )!=-1){

            $('#'+pks[i]).attr('checked',true)
        }
      }

      if(marks.length==pks.length){
        $('.day').prop("checked",true)
      }

  }
});
  
  
  }
  else{
    var reason=$("button[status='enable']").attr('reason')
    $.ajax({

      url:$('#dropdownMenuButton').attr('save_reason_url'),
      method:'get',
      data:{student:$(this).attr('student_pk'),day:$(this).attr('date_at'),month:$('.block').attr('month_at'),year:$('.block').attr('year_at'),reason:reason}



    })

    if (reason==3){
      $(this).addClass('bg-success text-white')
    }

    if (reason==2){
      $(this).addClass('bg-danger text-white')
    }

    if (reason==1){
      $(this).addClass('bg-info text-white')
    }

  }

})


$('.dropdown-item').click(function(){
    $("button[status='enable']").attr('status','disabled')
    $(this).attr('status','enable')
    $("#notice").removeClass('active')
    $('#dropdownMenuButton').addClass('active')
    

})


$('#notice').on('click',function(){
    $("button[status='enable']").attr('status','disabled');
    $(this).attr('status','enable');
    $("#dropdownMenuButton").removeClass('active');
    
    
   
    

    

})






});



function save_mark(self,url,tocken, min_mark,max_mark){
    
    $(self).css('display','none')
    var old_mark=$(self).attr('old_mark').replace(/\s+/g, '')
    var new_mark=$(self).val().replace(/\s+/g, '')
    var error=false
    var skip=false
    var attendance=0
    var text_mark=new_mark
    var new_mark=new_mark.split("/");
    var td_id=$(self).attr('td')
    $('#'+td_id).children('a').css('display','block')


    if(new_mark==old_mark){
      skip=true
    }

    if (new_mark[0]>max_mark | new_mark[0]<min_mark | new_mark[1]>max_mark | new_mark[1]<min_mark | isNaN(new_mark[0]) )
    {
      error=true
    }
    if (new_mark[0]=='н' | new_mark[0]=='н/а' | new_mark[0]==''){
      error=false
    }


    if (!error & !skip){

      var student=$('#'+td_id).attr('student')
      var type=0
      var lesson=0
      var red_mark=0
      var del_mark=0
      var itog=0
      var isitog=0
      $('#'+td_id).children('a').text(text_mark)
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
      
      
      
      if (old_mark!=new_mark & old_mark!='' & new_mark!='' ){
        red_mark=$('#'+td_id).attr('markpk')
      }
      
      if (old_mark!='' & new_mark=='' ){

        del_mark=$('#'+td_id).attr('markpk')
      }
      if(new_mark=='н' & itog==0){
        
        new_mark=0
        attendance=1
      }
      if(text_mark=='н/а' & itog!=0){
        new_mark=0
        attendance=1
      }
      
      if((text_mark=='н/а' & itog==0) | (new_mark=='н' & itog!=0)){
        $('#liveToast').toast('show');
      }

      else{

      
      two_mark=new_mark[1]
      first_mark=new_mark[0]
      if (!two_mark){
        two_mark=0
      }
      if (!first_mark){
        first_mark=0
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
        mark: first_mark,
        two_mark:two_mark,
        student:student,
        type:type,
        lesson:lesson,
        csrfmiddlewaretoken: tocken
      },

        success: function(data){

        var student=$('#'+td_id).attr('student')
        var marks=$('.'+student).text()
        var mark_sum=0
        var mark_lenght=0
        
        
        for (i = 0; i < marks.length; i +=1 ) {

            if(parseInt(marks[i])>0){

            mark_sum=mark_sum+parseInt(marks[i])
            mark_lenght+=1
          }
        }
        var ball=mark_sum/mark_lenght
         
        ball=ball.toFixed(2)
         
         if(ball>0){
            $('#ball'+student).text(ball)
       }

       $('#'+td_id).attr('markpk',data)

      }
  });

    }
}

else if(!skip){
  $('#liveToast').toast('show');
}

}


function click_mark(self){

  var td=$(self)
  var td_id=td.attr('id')
  var old_mark=$(td).children('a').text().replace(/\s+/g, '')

  var dayTop=$(self).offset().top
  var dayLeft=$(self).offset().left
  var dayWidth=$(self).css('width')
  var dayHeight=$(self).css('height')
  var mark=$(td).children('input')

  
  $(td).children('a').css('display','none')
  mark.val(old_mark)
  mark.css({'display':'block'}).focus()

  mark.attr({'old_mark':old_mark,'td':td_id})
  mark.focus()
  $(td).css('padding',0)
  
}