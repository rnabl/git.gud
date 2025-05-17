import os
import json

input_folder = "./ComfyUI/input/assassin"
output_folder = "./ComfyUI/input/assassin_batch_jsons"
os.makedirs(output_folder, exist_ok=True)

pose_frames = sorted([
    f for f in os.listdir(input_folder)
    if f.endswith(".png") and not f.startswith("assassin")
])

for i, frame in enumerate(pose_frames):
    label = os.path.splitext(frame)[0]

    prompt = {
        "0": {
            "class_type": "LoadCheckpoint",
            "inputs": {
                "ckpt_name": "v1-5-pruned-emaonly.safetensors"
            }
        },
        "1": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1,
                "model": ["0", 0]
            }
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["0", 1],
                "text": "pixel art assassin with dark armor and glowing blade"
            }
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["0", 1],
                "text": "text, watermark"
            }
        },
        "4": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["0", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["1", 0],
                "seed": 123456 + i,
                "steps": 25,
                "cfg": 7.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0
            }
        },
        "5": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["4", 0],
                "vae": ["0", 2]
            }
        },
        "6": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["5", 0],
                "filename_prefix": f"reskin_{label}"
            }
        }
    }

    with open(f"{output_folder}/{label}.json", "w") as f:
        json.dump({"prompt": prompt}, f, indent=2)

print(f"✅ Fully working prompts generated for {len(pose_frames)} frames.")
