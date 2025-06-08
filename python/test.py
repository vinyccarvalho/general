import os

nfs_path = "/mnt/tcloud_backup_restore"
pipeline_id = "24234273"

rubrik_bin_dir = os.path.join(nfs_path, pipeline_id, nfs_path.lstrip("/"))
print(rubrik_bin_dir)
