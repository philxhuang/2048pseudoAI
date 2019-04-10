        while index < len(curRow):
            if curRow[index] == self.fill:
                 curRow.pop(index)
                 curRow.append(self.fill)
            else:
                index += 1