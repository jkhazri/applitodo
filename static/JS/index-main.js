var Edit = document.getElementsByClassName('edit');
var Delete = document.getElementsByClassName('delete');
var Done = document.getElementsByClassName('done');

var Modal_Edit = document.querySelector('#Modal-Edit');
var Modal_Delete = document.querySelector('#Modal-Delete');


var CloseModal_edit = document.querySelector('#Close-Modal');
var CloseModal_delete = document.querySelector('#Close-Modal-edit');


// ------------- edit section START -------------
for (let i = 0 ; i < Edit.length; i++)
{   
    Edit[i].addEventListener('click',function(){
        Modal_Edit.style.display="block";
    })
}

CloseModal_edit.addEventListener('click',function(){
    Modal_Edit.style.display="none";
    
})
// ------------- edit section END -------------


// +++++++++++++ delete section Start ++++++++++++
for(let i = 0 ; i< Delete.length; i++)
{   
    Delete[i].addEventListener('click', function(){
        Modal_Delete.style.display="block";
    })
}

CloseModal_delete.addEventListener('click',function(){
    Modal_Delete.style.display="none";
    
})

// +++++++++++++ delete section END++++++++++++
