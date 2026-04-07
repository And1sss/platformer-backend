using UnityEngine;

public class ApiLoginTest : MonoBehaviour
{
    [SerializeField] private ApiClient apiClient;

    private int currentAttemptId;

    private void Start()
    {
        Login();
    }

    public void Login()
    {
        LoginRequest request = new LoginRequest
        {
            email = "test1@example.com",
            password = "password123"
        };

        StartCoroutine(apiClient.Post<LoginRequest, LoginResponseData>(
            "/api/v1/auth/login",
            request,
            onSuccess: data =>
            {
                apiClient.SetToken(data.accessToken);
                Debug.Log("LOGIN OK");
                Debug.Log("Token: " + data.accessToken);

                LoadProfile();
            },
            onError: error =>
            {
                Debug.LogError($"LOGIN ERROR: {error.code} | {error.message} | req={error.requestId}");
            }
        ));
    }

    public void LoadProfile()
    {
        StartCoroutine(apiClient.Get<ProfileResponseData>(
            "/api/v1/profile",
            onSuccess: data =>
            {
                Debug.Log("PROFILE OK");
                Debug.Log($"User: {data.user.nickname}");
                Debug.Log($"Level: {data.progress.level}");
                Debug.Log($"XP: {data.progress.xp}");
                Debug.Log($"SoftCurrency: {data.progress.softCurrency}");

                StartLevel();
            },
            onError: error =>
            {
                Debug.LogError($"PROFILE ERROR: {error.code} | {error.message} | req={error.requestId}");
            }
        ));
    }

    public void StartLevel()
    {
        LevelStartRequest request = new LevelStartRequest
        {
            levelCode = "level_01",
            clientVersion = "1.0.0"
        };

        StartCoroutine(apiClient.Post<LevelStartRequest, LevelStartResponseData>(
            "/api/v1/level/start",
            request,
            onSuccess: data =>
            {
                currentAttemptId = data.attemptId;
                Debug.Log("LEVEL START OK");
                Debug.Log($"AttemptId: {data.attemptId}");
                Debug.Log($"Status: {data.status}");

                FinishLevel();
            },
            onError: error =>
            {
                Debug.LogError($"LEVEL START ERROR: {error.code} | {error.message} | req={error.requestId}");
            }
        ));
    }

    public void FinishLevel()
    {
        LevelFinishRequest request = new LevelFinishRequest
        {
            attemptId = currentAttemptId,
            result = new LevelFinishResult
            {
                isCompleted = true,
                score = 2100,
                durationSeconds = 135,
                coinsCollected = 20,
                enemiesDefeated = 7,
                deathsCount = 1
            }
        };

        StartCoroutine(apiClient.Post<LevelFinishRequest, LevelFinishResponseData>(
            "/api/v1/level/finish",
            request,
            onSuccess: data =>
            {
                Debug.Log("LEVEL FINISH OK");
                Debug.Log($"AttemptId: {data.attemptId}");
                Debug.Log($"Completed: {data.isCompleted}");
                Debug.Log($"XP Gained: {data.xpGained}");
                Debug.Log($"Soft Currency Gained: {data.softCurrencyGained}");
            },
            onError: error =>
            {
                Debug.LogError($"LEVEL FINISH ERROR: {error.code} | {error.message} | req={error.requestId}");
            }
        ));
    }
}