let isEditable = false;

$(".select").select2({
    theme: "bootstrap4"
});

function restore() {
    $('form').find(':input').each(function(i, elem) {
        let input = $(elem);
        input.val(input.data('initialState'));
        input.trigger("change");
    });
}

$(document).ready(() => {

    $('form').find(':input').each(function(i, elem) {
        let input = $(elem);
        input.data('initialState', input.val());
    });

    $('#btn-editar').on('click', () => {
        if(isEditable){
            restore();
            $("input, select").prop('disabled', true);
            $('#btn-editar').text('Editar');
            $('#btn-cadastro').addClass('d-none');
            isEditable = false;
        }
        else{
            $("input, select").prop('disabled', false);
            $('#btn-editar').text('Desfazer alterações');
            $('#btn-cadastro').removeClass('d-none');
            isEditable = true;
        }
    })
});