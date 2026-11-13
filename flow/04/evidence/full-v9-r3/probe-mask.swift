import Foundation
import Vision
import CoreImage
import AppKit
let u=URL(fileURLWithPath:CommandLine.arguments[1]);let src=CIImage(contentsOf:u)!
let r=VNGeneratePersonSegmentationRequest();r.qualityLevel = .accurate;r.outputPixelFormat=kCVPixelFormatType_OneComponent8
let f=VNDetectFaceRectanglesRequest()
try VNImageRequestHandler(ciImage:src).perform([r,f])
let ctx=CIContext();let mask=CIImage(cvPixelBuffer:r.results![0].pixelBuffer).transformed(by:CGAffineTransform(scaleX:src.extent.width/CGFloat(CVPixelBufferGetWidth(r.results![0].pixelBuffer)),y:src.extent.height/CGFloat(CVPixelBufferGetHeight(r.results![0].pixelBuffer))))
try ctx.writePNGRepresentation(of:mask,to:URL(fileURLWithPath:CommandLine.arguments[2]),format:.RGBA8,colorSpace:CGColorSpaceCreateDeviceRGB())
for a in f.results ?? [] {print(a.boundingBox)}
