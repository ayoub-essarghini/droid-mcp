import xml.etree.ElementTree as ET
from typing import Any, Dict, List


class AndroidUIParser:
    """
    Parses raw Android UI Automator XML dumps into clean, LLM-friendly JSON.
    Filters out structural layouts and invisible elements to save tokens.
    """

    @staticmethod
    def parse_xml_to_json(xml_content: str) -> List[Dict[str, Any]]:
        try:
            # Handle empty or invalid XML
            if not xml_content or "hierarchy" not in xml_content:
                return []

            # Find the start of the actual XML (uiautomator sometimes prepends text)
            xml_start = xml_content.find("<?xml")
            if xml_start != -1:
                xml_content = xml_content[xml_start:]

            root = ET.fromstring(xml_content)
            elements = []
            element_id = 0

            # Iterate through all nodes in the XML tree
            for node in root.iter("node"):
                attrib = node.attrib

                # Skip invisible or empty elements to keep context clean
                bounds = attrib.get("bounds", "[0,0][0,0]")
                if bounds == "[0,0][0,0]" or bounds == "[0,0][0,0][0,0][0,0]":
                    continue

                text = attrib.get("text", "")
                content_desc = attrib.get("content-desc", "")
                is_clickable = attrib.get("clickable", "false") == "true"
                is_scrollable = attrib.get("scrollable", "false") == "true"
                is_checkable = attrib.get("checkable", "false") == "true"

                # We only care about nodes that have text, descriptions, or can be interacted with
                if text or content_desc or is_clickable or is_scrollable or is_checkable:
                    # Clean the bounds format from "[x1,y1][x2,y2]"
                    clean_bounds = (
                        bounds.replace("][", ",")
                        .replace("[", "")
                        .replace("]", "")
                        .split(",")
                    )

                    element_data = {
                        "id": element_id,
                        # E.g., 'Button' instead of 'android.widget.Button'
                        "class": attrib.get("class", "").split(".")[-1],
                        "text": text if text else None,
                        "description": content_desc if content_desc else None,
                        "clickable": is_clickable,
                        "bounds": (
                            [int(c) for c in clean_bounds]
                            if len(clean_bounds) == 4
                            else bounds
                        )
                    }

                    # Remove None values to make the JSON even smaller
                    element_data = {
                        k: v for k, v in element_data.items()
                        if v is not None and v is not False
                    }

                    elements.append(element_data)
                    element_id += 1

            return elements
        except ET.ParseError as e:
            print(f"XML Parsing Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected Parsing Error: {e}")
            return []
