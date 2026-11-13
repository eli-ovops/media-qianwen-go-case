import Foundation
import Vision
import CoreImage
import CoreVideo
let w=540,h=960,n=w*h*4
let context=CIContext(options:[.cacheIntermediates:false])
let request=VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat=kCVPixelFormatType_OneComponent8
let handler=VNSequenceRequestHandler()
let threshold=CIColorKernel(source:"kernel vec4 threshold(__sample s) { return vec4(vec3(step(0.85, s.r)), 1.0); }")!
let input=FileHandle.standardInput,output=FileHandle.standardOutput
let bg=CIImage(color:CIColor(red:9.0/255,green:13.0/255,blue:17.0/255)).cropped(to:CGRect(x:0,y:0,width:w,height:h))
var frame=0
while true {
 var data=Data()
 while data.count<n {let chunk=input.readData(ofLength:n-data.count);if chunk.isEmpty{break};data.append(chunk)}
 if data.isEmpty {break}
 if data.count != n {fatalError("partial frame")}
 try autoreleasepool {
  var pb:CVPixelBuffer?;CVPixelBufferCreate(nil,w,h,kCVPixelFormatType_32BGRA,[kCVPixelBufferIOSurfacePropertiesKey:[:] ] as CFDictionary,&pb)
  let pixel=pb!;CVPixelBufferLockBaseAddress(pixel,[])
  data.withUnsafeBytes { ptr in
   for y in 0..<h {memcpy(CVPixelBufferGetBaseAddress(pixel)!.advanced(by:y*CVPixelBufferGetBytesPerRow(pixel)),ptr.baseAddress!.advanced(by:y*w*4),w*4)}
  };CVPixelBufferUnlockBaseAddress(pixel,[])
  try handler.perform([request],on:pixel,orientation:.up)
  guard let observation=request.results?.first else {fatalError("no mask")}
  let source=CIImage(cvPixelBuffer:pixel)
  var mask=CIImage(cvPixelBuffer:observation.pixelBuffer)
  mask=mask.transformed(by:CGAffineTransform(scaleX:CGFloat(w)/mask.extent.width,y:CGFloat(h)/mask.extent.height))
  mask=threshold.apply(extent:mask.extent,arguments:[mask])!
  mask=mask.applyingFilter("CIMorphologyMinimum",parameters:[kCIInputRadiusKey:1.0])
  mask=mask.applyingFilter("CIGaussianBlur",parameters:[kCIInputRadiusKey:0.5])
  let result=source.applyingFilter("CIBlendWithMask",parameters:[kCIInputBackgroundImageKey:bg,kCIInputMaskImageKey:mask])
  var bytes=[UInt8](repeating:0,count:n)
  context.render(result,toBitmap:&bytes,rowBytes:w*4,bounds:CGRect(x:0,y:0,width:w,height:h),format:.BGRA8,colorSpace:CGColorSpaceCreateDeviceRGB())
  output.write(Data(bytes))
 }
 frame+=1
 if frame%120==0{FileHandle.standardError.write(Data("MATTE \(frame)\n".utf8))}
}
FileHandle.standardError.write(Data("COMPLETE \(frame)\n".utf8))
