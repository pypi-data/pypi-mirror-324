import cv2
import numpy as np
from typing import List, Optional, Union
from dataclasses import dataclass
import os

@dataclass

class QRResult:
    """คลาสสำหรับเก็บผลลัพธ์จากการอ่าน QR code"""
    data: bytes
    def decode(self, encoding: str = 'utf-8') -> Optional[str]:
        """แปลงข้อมูลไบต์เป็นสตริง"""
        try:
            return self.data.decode(encoding)
        except UnicodeDecodeError:
            return None

class QRDetectorError(Exception):
    """คลาสสำหรับข้อผิดพลาดที่เกิดในโมดูล QR Detector"""
    pass
class QRDetector:
    def init(self, debug: bool = False):
        self.qr_detector = cv2.QRCodeDetector()
        self.debug = debug
    def read_from_file(self, file_path: str) -> List[QRResult]:
        """
        อ่าน QR code จากไฟล์รูปภาพ
        Args:
            file_path: พาธของไฟล์รูปภาพ
        Returns:
            List[QRResult]: รายการผลลัพธ์ที่อ่านได้
        Raises:
            QRDetectorError: เมื่อเกิดข้อผิดพลาดในการอ่านหรือถอดรหัส
        """
        try:
            # ตรวจสอบว่าไฟล์มีอยู่จริง
            if not os.path.exists(file_path):
                raise QRDetectorError(f"ไม่พบไฟล์: {file_path}")
            # อ่านรูปภาพ
            img = cv2.imread(file_path)
            if img is None:
                raise QRDetectorError(f"ไม่สามารถอ่านไฟล์รูปภาพได้: {file_path}")
            # ถอดรหัส QR
            return self.decode(img)
        except QRDetectorError:
            raise
        except Exception as e:
            if self.debug:
                print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {str(e)}")
            raise QRDetectorError(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {str(e)}")
    def decode(self, img: np.ndarray) -> List[QRResult]:
        """
        ถอดรหัส QR code จากรูปภาพ numpy array
        Args:
            img: รูปภาพในรูปแบบ numpy array (BGR format)
        Returns:
            List[QRResult]: รายการผลลัพธ์ที่อ่านได้
        """
        try:
            if img is None or img.size == 0:
                raise QRDetectorError("รูปภาพไม่ถูกต้อง")
            # ถอดรหัส QR
            retval, decoded_info, points, straight_qrcode = self.qr_detector.detectAndDecodeMulti(img)
            results = []
            if retval:
                for data in decoded_info:
                    if data:  # ข้ามข้อมูลที่เป็น empty string
                        results.append(QRResult(data.encode('utf-8')))
            return results
        except Exception as e:
            if self.debug:
                print(f"เกิดข้อผิดพลาดในการถอดรหัส: {str(e)}")
            raise QRDetectorError(f"เกิดข้อผิดพลาดในการถอดรหัส: {str(e)}")

    async def read_from_bytes(self, img_bytes: bytes) -> List[QRResult]:
        """
        อ่าน QR code จากข้อมูลไบต์ของรูปภาพ       
        Args:
            img_bytes: ข้อมูลไบต์ของรูปภาพ
        Returns:
            List[QRResult]: รายการผลลัพธ์ที่อ่านได้
        """

        try:
            if not img_bytes:
                raise QRDetectorError("ไม่พบข้อมูลรูปภาพ")
            # แปลงไบต์เป็น numpy array
            nparr = np.frombuffer(img_bytes, np.uint8)

            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise QRDetectorError("ไม่สามารถแปลงข้อมูลไบต์เป็นรูปภาพได้")
            return self.decode(img)

        except QRDetectorError:
            raise
        except Exception as e:

            if self.debug:
                print(f"เกิดข้อผิดพลาดในการอ่านข้อมูลไบต์: {str(e)}")
            raise QRDetectorError(f"เกิดข้อผิดพลาดในการอ่านข้อมูลไบต์: {str(e)}")