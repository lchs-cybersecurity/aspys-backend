$(document).ready(function() {
    $("#login-button").click(function(event) {
        event.preventDefault()
        if (validate()) {
            $("#login-form").submit()
        } 
    })
    removeRedOnFocus()
})

function validate() {
    let badFields = {}
    for (let id of getFields()) {
        let status = validateInput($("#"+id))
        if (status != "ok") {
            badFields[id] = status
            continue
        }
    }
    if ($.isEmptyObject(badFields)) {
        return true
    } else {
        addRed(Object.keys(badFields))
        setErrorMessage(badFields)
        return false
    }
}

function validateInput($input) {
    let val = $input.val()
    if (val.length < 1) {
        return "empty"
    }
    return "ok"
}

function setErrorMessage(errors) {
    console.log(errors)
}

function removeRedOnFocus() {
    for (let id of getFields()) {
        $("#"+id).focus(function() {
            $(this).removeClass("red")
            $label(id).removeClass("red")
        })
    }
}

function getFields() {
    let fields = []
    $("input").each(function(i) {
        fields.push($(this).attr("id"))
    })
    return fields
}

function addRed(ids) {
    for (let id of ids) {
        $("#"+id).addClass("red")
        $label(id).addClass("red")
    }
}

function $label(id) {
    return $("label[for="+id+"]")
}