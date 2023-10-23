details_template = """
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <th style="border: 1px solid black; padding: 5px;">Attribute</th>
            <th style="border: 1px solid black; padding: 5px;">Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Ship Name</td>
            <td style="border: 1px solid black; padding: 5px;">{ship_name}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Nationality</td>
            <td style="border: 1px solid black; padding: 5px;">{nationality}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Date</td>
            <td style="border: 1px solid black; padding: 5px;">{date}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Sunk by</td>
            <td style="border: 1px solid black; padding: 5px;">{uboat}, commanded by: {commander}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Tonnage</td>
            <td style="border: 1px solid black; padding: 5px;">{tonnage}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Convoy</td>
            <td style="border: 1px solid black; padding: 5px;">{convoy}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Sunk coordinates</td>
            <td style="border: 1px solid black; padding: 5px;">{coordinates}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Map</td>
            <td style="border: 1px solid black; padding: 5px;"><a href='{map_html}'>Open Map</a></td>
        </tr>
    </table>
    """

statistics_template = """
    <h3>Statistics</h3>
    <p>Total Ships: {total_ships}</p>
    <p>Total Tonnage: {total_tonnage:,}</p>
    <p>Most common nationality: {most_common_nationality} ({nationality_count})</p>
    <p>Most active U-Boat: {most_common_uboat} ({uboat_count})</p>
    <p>Most successful commander: {most_common_commander} ({commander_count})</p>
    """
