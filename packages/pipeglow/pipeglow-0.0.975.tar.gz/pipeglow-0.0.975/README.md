# 🚀 pipeglow
> Visualize CI pipeline status with smart lights

## 🗺️ Overview

`pipeglow` updates your smart lights to provide real-time visual feedback about your CI pipeline status. By automatically changing light colors based on pipeline states, you get immediate visual notifications about how your builds and deployments are going.

## 🛠️ Installation

```bash
pip install pipeglow
```

## 📋 Configuration

Create a `.env` file with the following environment variables:

```bash
GOVEE_API_KEY=your_api_key_here
GOVEE_DEVICE_ID=your_device_id
GOVEE_DEVICE_MODEL=your_device_model
GITLAB_API_TOKEN=your_gitlab_token
GITLAB_PROJECT_ID=your_project_id
```

## ✨ Features

### 🌈 Pipeline Status Colors

Each pipeline state is represented by a distinct color:
- 💛 Preparing/Pending: Yellow (`#9F9110`)
- 💗 Waiting: Pink (`#DC6BAD`)
- 💙 Running: Blue (`#3974C6`)
- 💚 Success: Green (`#309508`)
- ❌ Failed: Red (`#FF0000`)
- ⚫ Canceled/Skipped: Dark Gray (`#212121`)

### 🌞 Dynamic Brightness

Light brightness automatically adjusts based on pipeline update recency:
- Recent updates appear brighter
- Brightness gradually dims as updates age
- Provides intuitive temporal feedback

### 🦊 GitLab Integration

There is support for checking any GitLab instance (`.com`, self-managed or GitLab Dedicated). By default, `pipeglow` assumes `gitlab.com`.

### 💡 Lighting Integration

Today, `pipeglow` works with Govee lights. You will need a [Govee API key](https://developer.govee.com/reference/apply-you-govee-api-key) in order to use `pipeglow`. You will need to run `pipeglow` on a machine with access to the Internet so that it can communicate with the Govee API.

## 🚀 Usage

This will cause `pipeglow` to check the project you specified in `.env` and update the light specified in `.env` accordingly. (Alternately, you can set the items specified in `.env` as environment variables.)

```bash
pipeglow change_the_lights
```

Specify a different GitLab URL:

```bash
pipeglow change_the_lights --gitlab-url https://gitlab.example.com
```

```bash
uvx pipeglow change_the_lights
```

Run a command like this in a loop to check and update the lights once every 15 seconds:

```bash
while true; do
    uvx pipeglow change_the_lights
    sleep 15
done
```

Alternately, you can use `set_the_lights` to set the lights based on a pipeline status. This is useful if you have a webhook trigger `pipeglow`.

```
uvx pipeglow set_the_lights success
```

``` 
# pipeglow set_the_lights  --light-status running
🚀 Just set the lights to running please!
🏆 The light has been updated!
```


## 📄 License

MIT License
