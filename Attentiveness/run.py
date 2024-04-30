import head_pose
import detection
import threading as th

if __name__ == "__main__":
    head_pose_thread = th.Thread(target=head_pose.pose)
    detection_thread = th.Thread(target=detection.run_detection)

    head_pose_thread.start()
    detection_thread.start()

    head_pose_thread.join()
    detection_thread.join()
