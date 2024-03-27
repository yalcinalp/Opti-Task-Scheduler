function showNextQuestion(currentQuestion) {
    var current = document.getElementById('question' + currentQuestion);
    var next = document.getElementById('question' + (currentQuestion + 1));

    if (current) {
        current.style.display = 'none';
    }

    if (next) {
        next.style.display = 'block';
    }
}

function submitSurvey() {
    alert('Survey completed!');
}

function next_question_wrapper(i) {

    return function showNextQuestion() {
        var current = document.getElementById('question' + i);
        var next = document.getElementById('question' + (i + 1));
    
        if (current) {
            current.style.display = 'none';
        }
    
        if (next) {
            next.style.display = 'block';
        }
    }
    
}



// Handle star rating selection
document.querySelectorAll('.rating').forEach(function(rating) {
    rating.addEventListener('click', function(e) {
        if (e.target.classList.contains('star')) {
            // Remove selected class from all stars
            this.querySelectorAll('.star').forEach(function(star) {
                star.classList.remove('selected');
            });

            // Add selected class to clicked star and previous stars
            e.target.classList.add('selected');
            let selectedValue = e.target.dataset.value;
            for (let i = 0; i < selectedValue - 1; i++) {
                this.children[i].classList.add('selected');
            }
        }
    });
});


document.getElementById("btn10").onclick = next_question_wrapper(1);
document.getElementById("btn11").onclick = next_question_wrapper(2);
document.getElementById("btn12").onclick = submitSurvey;