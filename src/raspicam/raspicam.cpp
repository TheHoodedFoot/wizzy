/**
 * @file raspicam.cpp
 *
 * @brief Raspberry Pi streaming server with OpenCV calibration
 *
 * Uses libcamera to capture and encode images, OpenCV to calibrate the camera,
 * and Apriltags to detect fiducial markers.
 *
 * Outline:
 * 1. Use libcamera to detect cameras and setup a camera.
 * 2. Create an event loop using libevent.
 * 3. Within the event loop, use libcamera to capture a frame.
 * 4. Use OpenCV to remove distortion from the image using existing calibration data
 * 5. Use Apriltags to detect any fiducials in the image
 * 6. Use OpenCV to highlight the detected fiducials.
 * 7. Use the Raspberry Pi's H.264 hardware encoder to encode the image
 * 8. Stream the encoded image over the network.
 * 9. Notify the client of any detected fiducials.
 *
 */

#include <iostream>
#include <libcamera/camera.h>
#include <libcamera/camera_manager.h>
#include <libcamera/control_list.h>
#include <libcamera/framebuffer_allocator.h>
#include <libcamera/request.h>
#include <libcamera/stream.h>

using namespace libcamera;

// Function prototypes
void requestComplete(Request *request);
std::string cameraName(Camera *camera);

int main()
{
    // Create a Camera Manager
    std::unique_ptr<CameraManager> cm = std::make_unique<CameraManager>();
    cm->start();

    // List available cameras
    for (auto const &camera : cm->cameras())
        std::cout << " - " << cameraName(camera.get()) << std::endl;

    // Check if there are any cameras available
    if (cm->cameras().empty()) {
        std::cout << "No cameras were identified on the system." << std::endl;
        cm->stop();
        return EXIT_FAILURE;
    }

    // Get the first camera
    Camera *camera = cm->cameras()[0];
    camera->acquire();

    // Generate a configuration for the camera
    std::unique_ptr<CameraConfiguration> config =
        camera->generateConfiguration({StreamRole::Viewfinder});

    // Validate and apply the configuration
    config->validate();
    camera->configure(config.get());

    // Allocate buffers
    FrameBufferAllocator *allocator = new FrameBufferAllocator(camera);
    for (StreamConfiguration &cfg : *config) {
        int ret = allocator->allocate(cfg.stream());
        if (ret < 0) {
            std::cerr << "Can't allocate buffers" << std::endl;
            return EXIT_FAILURE;
        }
    }

    // Create and queue requests
    Stream *stream = config->at(0).stream();
    const std::vector<std::unique_ptr<FrameBuffer>> &buffers = allocator->buffers(stream);
    std::vector<std::unique_ptr<Request>> requests;
    for (unsigned int i = 0; i < buffers.size(); ++i) {
        std::unique_ptr<Request> request = camera->createRequest();
        if (!request) {
            std::cerr << "Can't create request" << std::endl;
            return EXIT_FAILURE;
        }

        const std::unique_ptr<FrameBuffer> &buffer = buffers[i];
        int ret = request->addBuffer(stream, buffer.get());
        if (ret < 0) {
            std::cerr << "Can't set buffer for request" << std::endl;
            return EXIT_FAILURE;
        }

        ControlList &controls = request->controls();
        controls.set(controls::Brightness, 0.5);

        requests.push_back(std::move(request));
    }

    // Connect the request completed signal
    camera->requestCompleted.connect(requestComplete);

    // Start the camera and queue requests
    camera->start();
    for (std::unique_ptr<Request> &request : requests)
        camera->queueRequest(request.get());

    // Run an event loop
    EventLoop loop;
    loop.timeout(10); // 10 seconds timeout
    int ret = loop.exec();
    std::cout << "Capture ran for 10 seconds and stopped with exit status: " << ret << std::endl;

    // Clean up
    camera->stop();
    allocator->free(stream);
    delete allocator;
    camera->release();
    cm->stop();

    return EXIT_SUCCESS;
}

// Function definitions
void requestComplete(Request *request)
{
    std::cout << "Request completed" << std::endl;
}

std::string cameraName(Camera *camera)
{
    const ControlList &props = camera->properties();
    std::string name;

    const auto &location = props.get(properties::Location);
    if (location) {
        switch (*location) {
        case properties::CameraLocationFront:
            name = "Internal front camera";
            break;
        case properties::CameraLocationBack:
            name = "Internal back camera";
            break;
        default:
            name = "Unknown location camera";
            break;
        }
    } else {
        name = "No location information";
    }

    return name + " (" + camera->id() + ")";
}

/**
 * @brief Capture a frame from the camera
 *
 * This function captures a single frame from the camera using libcamera.
 *
 * @param request The request object to capture the frame
 */
void captureFrame(Request *request)
{
    // TODO: Implement frame capturing logic
}

/**
 * @brief Remove distortion from the captured image
 *
 * This function uses OpenCV to remove distortion from the captured image
 * based on existing calibration data.
 *
 * @param frame The captured frame
 * @return The undistorted frame
 */
cv::Mat removeDistortion(const cv::Mat &frame)
{
    // TODO: Implement distortion removal logic
    return cv::Mat();
}

/**
 * @brief Detect fiducial markers in the image
 *
 * This function uses Apriltags to detect any fiducial markers in the image.
 *
 * @param frame The undistorted frame
 * @return A list of detected fiducials
 */
std::vector<AprilTag> detectFiducials(const cv::Mat &frame)
{
    // TODO: Implement fiducial detection logic
    return std::vector<AprilTag>();
}

/**
 * @brief Highlight the detected fiducials in the image
 *
 * This function uses OpenCV to highlight the detected fiducials in the image.
 *
 * @param frame The undistorted frame
 * @param fiducials The list of detected fiducials
 * @return The highlighted frame
 */
cv::Mat highlightFiducials(const cv::Mat &frame, const std::vector<AprilTag> &fiducials)
{
    // TODO: Implement highlighting logic
    return cv::Mat();
}

/**
 * @brief Encode the image using the Raspberry Pi's H.264 hardware encoder
 *
 * This function uses the Raspberry Pi's H.264 hardware encoder to encode the image.
 *
 * @param frame The highlighted frame
 * @return The encoded image
 */
std::vector<uint8_t> encodeImage(const cv::Mat &frame)
{
    // TODO: Implement encoding logic
    return std::vector<uint8_t>();
}

/**
 * @brief Stream the encoded image over the network
 *
 * This function streams the encoded image over the network to a client.
 *
 * @param encodedImage The encoded image
 */
void streamImage(const std::vector<uint8_t> &encodedImage)
{
    // TODO: Implement streaming logic
}

/**
 * @brief Notify the client of any detected fiducials
 *
 * This function notifies the client of any detected fiducials.
 *
 * @param fiducials The list of detected fiducials
 */
void notifyClient(const std::vector<AprilTag> &fiducials)
{
    // TODO: Implement notification logic
}
