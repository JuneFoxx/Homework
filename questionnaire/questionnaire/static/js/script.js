document.addEventListener('DOMContentLoaded', () => {
  const openBtn = document.getElementById('openModal');
  const closeBtn = document.getElementById('closeModal');
  const overlay = document.getElementById('modalOverlay');

  if (!openBtn || !closeBtn || !overlay) return;

  openBtn.onclick = () => {
    overlay.style.display = 'flex';
  };

  closeBtn.addEventListener('click', () => {
  overlay.style.display = 'none';

  const questionsContainer = document.getElementById('questions-container');
  const titleInput = document.getElementById('titleInput')

  if (titleInput) {
    titleInput.value = '';
  }

  if (questionsContainer) {
    questionsContainer.innerHTML = ''; 
  }
  });

  overlay.onclick = (e) => {
    if (e.target === overlay) {
      overlay.style.display = 'none';
    }
  };
});

let questionCount = 0;
document.getElementById('addQuestionModal').addEventListener('click', function() {
  const container = document.getElementById('questions-container');

  const questionDiv = document.createElement('div');
  questionDiv.className = 'question-block';

  questionCount++;

  questionDiv.innerHTML = `
    <label>
      Вопрос:
      <input type="text" name="questions[]" required />
    </label>
    <input type="hidden" name="question_ids[]" value="${questionCount}">
    <div class="answers-container"></div>
    <button type="button" class="addAnswerModal" data-question-id="${questionCount}">Добавить ответ</button>
    <hr>
  `;

  container.appendChild(questionDiv);

  const addAnswerBtn = questionDiv.querySelector('.addAnswerModal');

  addAnswerBtn.addEventListener('click', function() {
    const questionId = addAnswerBtn.getAttribute('data-question-id');
    const answersContainer = questionDiv.querySelector('.answers-container');

    const answerInput = document.createElement('input');
    answerInput.type = 'text';
    answerInput.name = `answers_${questionId}[]`;
    answerInput.required = true;

    answersContainer.appendChild(answerInput);
  });
});