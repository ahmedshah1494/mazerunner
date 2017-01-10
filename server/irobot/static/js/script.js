
$(document).ready(function () {
    // Ajax setup to forward the CSRF token
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // generate CSRF token using jQuery
            var csrftoken = $.cookie('csrftoken');
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

var new_sym_id = 2;
var current_symptoms;
var current_diseases;

function add_symptom() {
    var symptom_objs = $(".symptom");
    var check_objs = $(".sym-checks")
    var pid = $("#pid")[0].value;
    var symptoms = [];
    var checks = [];
    for (var i = 0; i < symptom_objs.length; i++)
        symptoms.push(symptom_objs[i].value);
    for (var i = 0; i < check_objs.length; i++)
        checks.push(check_objs[i].checked);

    var num_syms = symptom_objs.length;
    $("#form-list")[0].innerHTML +=
        '     <div class="row" id="sym-container-'+new_sym_id+'">' +
        '       <br/>' +
        '       <div class="input-group">' +
        '         <input type="text" class="form-control symptom" id="sym'+new_sym_id+'" placeholder="Symptom">' +
        '         <span class="input-group-addon">' +
        '           <input type="checkbox" aria-label="..." id="check'+new_sym_id+'" class="sym-checks" checked>' +
        '         </span>' +
        '         <span class="input-group-btn">' +
        '           <div style="margin" class="btn btn-danger" id="remove-sym-btn-btn" onclick="remove_symptom('+new_sym_id+');">-</div>' +
        '         </span>' +
        '       </div>' +
        '     </div>';
    new_sym_id += 1;

    symptom_objs = $(".symptom");
    check_objs = $(".sym-checks");
    for (var i = 0; i < symptom_objs.length - 1; i++)
        symptom_objs[i].value = symptoms[i];
    for (var i = 0; i < check_objs.length - 1; i++)
        check_objs[i].checked = checks[i];
    $("#pid")[0].value = pid;
}

function remove_symptom(id) {
    $("#sym-container-"+id).remove();
}

function diagnose(url) {
    $("#diagnose-btn").attr('disabled', true);
    $("#loading-img").show();
    $("#diagnose-text").hide();

    var symptom_objs = $(".symptom");
    var check_objs = $(".sym-checks")
    var pid = $("#pid")[0].value;
    var symptoms = [];
    for (var i = 0; i < symptom_objs.length; i++) {
        symptoms.push({
            "name": symptom_objs[i].value,
            "is_negative": !check_objs[i].checked,
        });
    }

    $.post(url, {
        "id": pid,
        "symptoms": JSON.stringify(symptoms),
    }, function(data) {
        data = JSON.parse(data);
        if (data["errorcode"] == 0) {
            $("#diseases")[0].innerHTML = "";
            current_diseases = data["result"]["diseases"];
            current_symptoms = data["result"]["symptoms"];

            for (i in data["result"]["diseases"]) {
                d = data["result"]["diseases"][i];
                var name = d["diseases"][0]["name"];
                for (var i = 1; i < d["diseases"].length; i++)
                    name += " and " + d["diseases"][i]["name"];
                var p = d["weight"] * 100;
                $("#diseases")[0].innerHTML +=
                    '<div class="progress">' +
                    '  <div class="progress-bar" role="progressbar" aria-valuenow="'+p+'" aria-valuemin="0" aria-valuemax="100" style="width: '+p+'%;">' +
                    '    <span class="disease-name">' + name + '</span>' +
                    '  </div>' +
                    '</div>';
            }

            $("#recommendations")[0].innerHTML = "";
            for (i in data["result"]["recommendations"]) {
                r = data["result"]["recommendations"][i];
                var name = r["symptom"];
                var dname = r["disease"];
                var p = r["weight"] * 100;
                $("#recommendations")[0].innerHTML += "<p>Does the patient have " + name + " (for " + dname + ")</p>";
            }
        } else {
            alert("Error: " + data["error"]);
        }

        $("#loading-img").hide();
        $("#diagnose-text").show();
        $("#diagnose-btn").attr('disabled', false);
    });
}

function submit_diagnosis(url) {
    var symptom_objs = $(".symptom");
    var check_objs = $(".sym-checks")
    var pid = $("#pid")[0].value;
    var diagnosis = $("#final-diagnosis")[0].value;
    var description = $("#diagnosis-description")[0].value;
    var diseases_objs = $(".disease-name");
    var diseases = JSON.stringify(current_diseases);
    var symptoms = JSON.stringify(current_symptoms);

    $.post(url, {
        "id": pid,
        "symptoms": symptoms,
        "diagnosis": diagnosis,
        "description": description,
        "diseases": diseases
    }, function(data) {
        data = JSON.parse(data);
        if (data["errorcode"] == 0) {

        } else {
            alert("Error: " + data["error"]);
        }

        $("#loading-img").hide();
        $("#diagnose-text").show();
        $("#diagnose-btn").attr('disabled', false);
    });
}

