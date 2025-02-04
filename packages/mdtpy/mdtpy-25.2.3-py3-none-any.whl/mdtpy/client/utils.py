from __future__ import annotations

from typing import Optional
from abc import ABC, abstractmethod

import time

from mdtpy.model import Reference

def semantic_id_string(semantic_id:Optional[Reference]) -> str:
    """
    Reference 객체에서 semantic ID 부분을 추출한다.

    Args:
        semantic_id (Optional[Reference]): 시맨틱 ID Reference 객체

    Returns:
        str: Semantic ID 문자열. semantic_id가 None인 경우 None을 반환
    """
    if semantic_id:
        return semantic_id.keys[0].value
    else:
        return None

class StatusPoller(ABC):
    """
    Abstract base class for polling the status of an operation.
    Attributes:
        poll_interval (float): The interval in seconds between each poll.
        timeout (Optional[float]): The maximum time in seconds to wait for the operation to complete. If None, wait indefinitely.
    Methods:
        check_done() -> bool:
            Abstract method to check if the operation is done. Must be implemented by subclasses.
        wait_for_done() -> None:
            Waits for the operation to complete by repeatedly calling `check_done` at intervals specified by `poll_interval`.
            Raises:
                TimeoutError: If the operation does not complete within the specified timeout.
    """
    def __init__(self, poll_interval:float, timeout:Optional[float]=None):
        self.poll_interval = poll_interval
        self.timeout = timeout
        
    @abstractmethod
    def check_done(self) -> bool: pass
    
    def wait_for_done(self) -> None:
        # 타임아웃 (self.timeout)이 있는 경우 최종 제한 시간을 계산하고,    
        # 타임아웃이 없는 경우 due를 None으로 설정하여 무제한 대기하도록 한다.
        started = time.time()
        due = started + self.timeout if self.timeout else None
        # 다음 폴링 시간을 계산한다.
        next_wakeup = started + self.poll_interval
        
        while not self.check_done():
            now = time.time()
            
            # 타임 아웃까지 남은 시간이 일정 시간 이내인 경우에는 TimeoutError를 발생시킨다.
            # 그렇지 않은 경우는 다음 폴링 시간까지 대기한다.
            if due and (due - now) < 0.01:
                raise TimeoutError(f'timeout={self.timeout}')
            
            # 다음 폴링 시간까지 남은 시간이 짧으면 대기하지 않고 바로 다음 폴링 시도한다.
            sleep_time = next_wakeup - now
            if sleep_time > 0.001:
                time.sleep(sleep_time)
            next_wakeup += self.poll_interval