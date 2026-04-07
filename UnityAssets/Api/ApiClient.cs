using System;
using System.Collections;
using System.Text;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Networking;

public class ApiClient : MonoBehaviour
{
    [SerializeField] private string baseUrl = "http://127.0.0.1:5000";

    public string AccessToken { get; private set; }

    public void SetToken(string token)
    {
        AccessToken = token;
        PlayerPrefs.SetString("accessToken", token);
        PlayerPrefs.Save();
        Debug.Log("TOKEN SAVED");
    }

    public void LoadSavedToken()
    {
        if (PlayerPrefs.HasKey("accessToken"))
        {
            AccessToken = PlayerPrefs.GetString("accessToken");
            Debug.Log("TOKEN LOADED: " + AccessToken);
        }
        else
        {
            AccessToken = null;
            Debug.Log("TOKEN NOT FOUND");
        }
    }

    public void ClearToken()
    {
        AccessToken = null;
        PlayerPrefs.DeleteKey("accessToken");
        PlayerPrefs.Save();
        Debug.Log("TOKEN CLEARED");
    }

    public IEnumerator Post<TRequest, TResponse>(
        string path,
        TRequest body,
        Action<TResponse> onSuccess,
        Action<ApiError> onError)
    {
        string url = baseUrl + path;
        string json = JsonConvert.SerializeObject(body);
        byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

        using UnityWebRequest request = new UnityWebRequest(url, "POST");
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();

        request.SetRequestHeader("Content-Type", "application/json");

        if (!string.IsNullOrEmpty(AccessToken))
        {
            request.SetRequestHeader("Authorization", "Bearer " + AccessToken);
        }

        request.timeout = 15;

        yield return request.SendWebRequest();

        string responseText = request.downloadHandler.text;

        if (request.result == UnityWebRequest.Result.ConnectionError ||
            request.result == UnityWebRequest.Result.DataProcessingError)
        {
            onError?.Invoke(new ApiError
            {
                code = "NETWORK_ERROR",
                message = request.error,
                requestId = null
            });
            yield break;
        }

        ApiResponse<TResponse> apiResponse = null;

        if (!string.IsNullOrEmpty(responseText))
        {
            try
            {
                apiResponse = JsonConvert.DeserializeObject<ApiResponse<TResponse>>(responseText);
            }
            catch
            {
                onError?.Invoke(new ApiError
                {
                    code = "BAD_JSON",
                    message = "Response is not valid JSON",
                    requestId = null
                });
                yield break;
            }
        }

        if (request.responseCode >= 200 && request.responseCode < 300)
        {
            if (apiResponse != null && apiResponse.ok)
            {
                onSuccess?.Invoke(apiResponse.data);
            }
            else
            {
                onError?.Invoke(apiResponse?.error ?? new ApiError
                {
                    code = "UNKNOWN_ERROR",
                    message = "Unknown API error",
                    requestId = null
                });
            }
        }
        else
        {
            onError?.Invoke(apiResponse?.error ?? new ApiError
            {
                code = "HTTP_ERROR",
                message = $"HTTP {request.responseCode}",
                requestId = null
            });
        }
    }

    public IEnumerator Get<TResponse>(
        string path,
        Action<TResponse> onSuccess,
        Action<ApiError> onError)
    {
        string url = baseUrl + path;

        using UnityWebRequest request = UnityWebRequest.Get(url);

        if (!string.IsNullOrEmpty(AccessToken))
        {
            request.SetRequestHeader("Authorization", "Bearer " + AccessToken);
        }

        request.timeout = 15;

        yield return request.SendWebRequest();

        string responseText = request.downloadHandler.text;

        if (request.result == UnityWebRequest.Result.ConnectionError ||
            request.result == UnityWebRequest.Result.DataProcessingError)
        {
            onError?.Invoke(new ApiError
            {
                code = "NETWORK_ERROR",
                message = request.error,
                requestId = null
            });
            yield break;
        }

        ApiResponse<TResponse> apiResponse = null;

        if (!string.IsNullOrEmpty(responseText))
        {
            try
            {
                apiResponse = JsonConvert.DeserializeObject<ApiResponse<TResponse>>(responseText);
            }
            catch
            {
                onError?.Invoke(new ApiError
                {
                    code = "BAD_JSON",
                    message = "Response is not valid JSON",
                    requestId = null
                });
                yield break;
            }
        }

        if (request.responseCode >= 200 && request.responseCode < 300)
        {
            if (apiResponse != null && apiResponse.ok)
            {
                onSuccess?.Invoke(apiResponse.data);
            }
            else
            {
                onError?.Invoke(apiResponse?.error ?? new ApiError
                {
                    code = "UNKNOWN_ERROR",
                    message = "Unknown API error",
                    requestId = null
                });
            }
        }
        else
        {
            onError?.Invoke(apiResponse?.error ?? new ApiError
            {
                code = "HTTP_ERROR",
                message = $"HTTP {request.responseCode}",
                requestId = null
            });
        }
    }
}

[Serializable]
public class ApiResponse<T>
{
    public bool ok;
    public T data;
    public ApiError error;
}

[Serializable]
public class ApiError
{
    public string code;
    public string message;
    public string requestId;
}

[Serializable]
public class RegisterRequest
{
    public string email;
    public string password;
    public string nickname;
}

[Serializable]
public class RegisterResponseData
{
    public int userId;
}

[Serializable]
public class LoginRequest
{
    public string email;
    public string password;
}

[Serializable]
public class LoginResponseData
{
    public string accessToken;
    public string tokenType;
    public int expiresInSeconds;
}

[Serializable]
public class ProfileResponseData
{
    public UserDto user;
    public ProgressDto progress;
}

[Serializable]
public class UserDto
{
    public int id;
    public string email;
    public string nickname;
    public string createdAt;
    public string lastLoginAt;
    public bool isBanned;
}

[Serializable]
public class ProgressDto
{
    public int level;
    public int xp;
    public int softCurrency;
    public int hardCurrency;
    public string updatedAt;
}

[Serializable]
public class LevelStartRequest
{
    public string levelCode;
    public string clientVersion;
}

[Serializable]
public class LevelStartResponseData
{
    public int attemptId;
    public string status;
}

[Serializable]
public class LevelFinishRequest
{
    public int attemptId;
    public LevelFinishResult result;
}

[Serializable]
public class LevelFinishResult
{
    public bool isCompleted;
    public int score;
    public int durationSeconds;
    public int coinsCollected;
    public int enemiesDefeated;
    public int deathsCount;
}

[Serializable]
public class LevelFinishResponseData
{
    public int attemptId;
    public bool isCompleted;
    public int xpGained;
    public int softCurrencyGained;
}

[Serializable]
public class LeaderboardResponseData
{
    public string boardCode;
    public int season;
    public List<LeaderboardItemDto> items;
}

[Serializable]
public class LeaderboardItemDto
{
    public int rank;
    public int userId;
    public string nickname;
    public int score;
}