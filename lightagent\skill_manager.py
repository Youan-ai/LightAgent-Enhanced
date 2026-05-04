"""
SkillManager — 目录即技能
==========================
自动发现 skills/ 目录下的 SKILL.md 文件，注册为可用技能。
支持手动注册和按类别筛选。
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SkillInfo:
    """Skill metadata."""
    name: str
    path: str
    description: str
    version: str = "1.0.0"
    category: str = "通用"
    dependencies: List[str] = field(default_factory=list)
    enabled: bool = True


class SkillManager:
    """Skill manager — directory-as-skill auto-discovery.

    Automatically scans skills/ directory for SKILL.md files
    and registers them as discoverable skills.
    """

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self._skills: Dict[str, SkillInfo] = {}
        self._manual_skills: Dict[str, SkillInfo] = {}

    def discover(self) -> List[SkillInfo]:
        """Auto-discover skills from the skills/ directory."""
        discovered = []
        base = os.path.abspath(self.skills_dir)

        if not os.path.isdir(base):
            return discovered

        for entry in os.listdir(base):
            skill_path = os.path.join(base, entry)
            skill_file = os.path.join(skill_path, "SKILL.md")

            if os.path.isdir(skill_path) and os.path.exists(skill_file):
                description = ""
                with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                    first_line = f.readline().strip()
                    description = first_line.lstrip("#").strip()

                info = SkillInfo(
                    name=entry,
                    path=skill_path,
                    description=description or f"Skill: {entry}",
                )
                self._skills[entry] = info
                discovered.append(info)

        return discovered

    def register(self, name: str, path: str, description: str = "",
                 category: str = "通用", dependencies: List[str] = None):
        """Manually register a skill."""
        info = SkillInfo(
            name=name, path=path, description=description,
            category=category, dependencies=dependencies or [],
        )
        self._manual_skills[name] = info
        return info

    def get(self, name: str) -> Optional[SkillInfo]:
        return self._skills.get(name) or self._manual_skills.get(name)

    def list_skills(self, category: Optional[str] = None) -> List[SkillInfo]:
        result = list(self._skills.values()) + list(self._manual_skills.values())
        if category:
            result = [s for s in result if s.category == category and s.enabled]
        return result

    def all_names(self) -> List[str]:
        return list(self._skills.keys()) + list(self._manual_skills.keys())

    def get_skill_path(self, name: str) -> Optional[str]:
        info = self.get(name)
        return info.path if info else None
