var input = document.getElementById('file-img');
var displayedImage = document.getElementById('img');
var subject = document.getElementById('subject');
var religionSelect = document.getElementById('religion');
var reliSpan = document.getElementById('reli');
var subjectCodeSpan = document.getElementById('subject-code-of-reli');
var year = document.getElementById('year');
var calss = document.getElementById('class');
var section = document.getElementById('section');
var roll = document.getElementById('roll');

document.getElementById('class').addEventListener('change', function() {
    subject.style.display = 'block';
});


religionSelect.addEventListener('change', function() {
    // Check the selected value and update the text accordingly

    var selectedValue = religionSelect.value;

    switch (selectedValue) {
        case 'Islam':
            reliSpan.textContent = 'Religion - Islam';
            subjectCodeSpan.textContent = '111';
            break;
        case 'Hindu':
            reliSpan.textContent = 'Religion - Hindu';
            subjectCodeSpan.textContent = '112';
            break;
        case 'Chistian':
            reliSpan.textContent = 'Religion - Christian';
            subjectCodeSpan.textContent = '113';
            break;
        case 'Buddha':
            reliSpan.textContent = 'Religion - Buddha';
            subjectCodeSpan.textContent = '114';
            break;
        default:
            reliSpan.textContent = 'Invalid Selection';
            subjectCodeSpan.textContent = '';
    }
});



function submitForm() {
    // Get form values
    yearN = year.value;
    sectionN = section.value;
    rollN = roll.value;
    calssN = calss.value;

    var studentId = document.getElementById('s-id');

    studentId.textContent = yearN + calssN + sectionN + rollN ;

};
function cancelForm() {
    var userResponse = window.confirm("Are you sure you want to cancel this form?");

if (userResponse) {
    // User clicked "OK" in the confirmation dialog
    // Execute the next code here
    location.reload()
} else {
    // User clicked "Cancel" in the confirmation dialog
    // Do something else or stop execution
    console.log("User clicked Cancel. Not executing next code.");
}
}
document.getElementById('file-img').addEventListener('change', function () {


    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            displayedImage.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    } else {
        // If no file is selected, you may choose to handle this case differently.
        // For now, setting a default image.
        displayedImage.src = 'images.png';
    }
});
