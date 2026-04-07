using TMPro;
using UnityEngine;

public class LevelRunController : MonoBehaviour
{
    [SerializeField] private ApiClient apiClient;

    [Header("Level config")]
    [SerializeField] private string levelCode = "level_01";
    [SerializeField] private string clientVersion = "1.0.0";

    [Header("UI")]
    [SerializeField] private TMP_Text statusText;
    [SerializeField] private TMP_Text rewardText;
    [SerializeField] private GameObject resultPanel;

    private int currentAttemptId;
    private float levelStartTime;
    private bool levelActive;

    private int coinsCollected;
    private int enemiesDefeated;
    private int deathsCount;
    private int score;

    private void Start()
    {
        apiClient.LoadSavedToken();

        if (resultPanel != null)
            resultPanel.SetActive(false);

        StartLevelOnServer();
    }

    public void AddCoin()
    {
        coinsCollected++;
    }

    public void AddEnemyDefeated()
    {
        enemiesDefeated++;
    }

    public void AddDeath()
    {
        deathsCount++;
    }

    public void AddScore(int value)
    {
        score += value;
    }

    public void FinishWin()
    {
        if (!levelActive) return;
        FinishLevel(true, score);
    }

    public void FinishLose()
    {
        if (!levelActive) return;
        FinishLevel(false, score);
    }

    private void StartLevelOnServer()
    {
        LevelStartRequest request = new LevelStartRequest
        {
            levelCode = levelCode,
            clientVersion = clientVersion
        };

        if (statusText != null)
            statusText.text = "Запуск уровня...";

        StartCoroutine(apiClient.Post<LevelStartRequest, LevelStartResponseData>(
            "/api/v1/level/start",
            request,
            onSuccess: data =>
            {
                currentAttemptId = data.attemptId;
                levelStartTime = Time.time;
                levelActive = true;

                if (statusText != null)
                    statusText.text = $"Уровень начат. AttemptId={currentAttemptId}";
            },
            onError: error =>
            {
                if (statusText != null)
                    statusText.text = $"Ошибка старта: {error.message}";
            }
        ));
    }

    private void FinishLevel(bool isCompleted, int finalScore)
    {
        levelActive = false;

        int durationSeconds = Mathf.RoundToInt(Time.time - levelStartTime);

        LevelFinishRequest request = new LevelFinishRequest
        {
            attemptId = currentAttemptId,
            result = new LevelFinishResult
            {
                isCompleted = isCompleted,
                score = finalScore,
                durationSeconds = durationSeconds,
                coinsCollected = coinsCollected,
                enemiesDefeated = enemiesDefeated,
                deathsCount = deathsCount
            }
        };

        if (statusText != null)
            statusText.text = "Отправка результата...";

        StartCoroutine(apiClient.Post<LevelFinishRequest, LevelFinishResponseData>(
            "/api/v1/level/finish",
            request,
            onSuccess: data =>
            {
                if (statusText != null)
                    statusText.text = isCompleted ? "Уровень завершён!" : "Попытка завершена";

                if (rewardText != null)
                    rewardText.text = $"+{data.xpGained} XP  +{data.softCurrencyGained} монет";

                if (resultPanel != null)
                    resultPanel.SetActive(true);
            },
            onError: error =>
            {
                if (statusText != null)
                    statusText.text = $"Ошибка финиша: {error.message}";
            }
        ));
    }
}